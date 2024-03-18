import datetime

from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import session

from entity import models, schemas
from service import groups as group_service


def get_todo_list(
        group_id: int, current_user: models.User, db: session, from_date_str: str, to_date_str: str
) -> list[schemas.TodoItemsGroupByDate]:
    if not group_service.is_user_in_group(current_user.id, group_id, db):
        raise HTTPException(403, detail="请先加入此团队")
    next_date_str = (datetime.datetime.strptime(to_date_str, "%Y-%m-%d") + datetime.timedelta(days=1)
                     ).strftime("%Y-%m-%d")
    query = db.query(models.TodoList).filter(models.TodoList.group_id == group_id,
                                                models.TodoList.start_time.between(from_date_str, next_date_str))
    if group_id == 0:
        query = query.filter(models.TodoList.user_id == current_user.id)
    db_items = query.order_by(
        desc(models.TodoList.id), desc(models.TodoList.id)).all()
    # 按日期分组
    result = list()
    current_key = ""
    for db_item in db_items:
        if current_key != (temp_key := db_item.start_time.strftime("%Y-%m-%d")) or current_key == "":
            current_key = temp_key
            result.append(schemas.TodoItemsGroupByDate(key=current_key, value=list()))
        else:
            current_key = db_item.start_time.strftime("%Y-%m-%d")
        result[-1].value.append(db_item)
    return result


def create_todo_item(item: schemas.TodoItemCreate, current_user: models.User, db: session) -> models.TodoList:
    if not group_service.is_user_in_group(current_user.id, item.group_id, db):
        raise HTTPException(403, detail="请先加入此团队")
    if item.is_all_day:
        item.start_time = item.start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        item.end_time = item.end_time.replace(hour=0, minute=0, second=0, microsecond=0)
    db_item = models.TodoList(**item.dict(), user_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_todo_item(item: schemas.TodoItemUpdate, current_user: models.User, db: session):
    db_item = db.query(models.TodoList).get(item.id)
    if not group_service.is_user_in_group(current_user.id, db_item.group_id, db):
        raise HTTPException(403, detail="请先加入此团队")
    if not db_item:
        raise HTTPException(404, "记录不存在")
    if item.is_all_day:
        item.start_time = item.start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        item.end_time = item.end_time.replace(hour=0, minute=0, second=0, microsecond=0)

    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    return db_item


def delete_todo_item(item_id: int, current_user: models.User, db: session):
    db_item = db.query(models.TodoList).get(item_id)
    if not group_service.is_user_in_group(current_user.id, db_item.group_id, db):
        raise HTTPException(403, detail="请先加入此团队")
    db.delete(db_item)
    db.commit()
