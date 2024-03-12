import math

from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import session

from entity import models, schemas
from service import groups as group_service


def get_todo_list(
        group_id: int, current_user: models.User, db: session, page: int, size: int
) -> schemas.AbstractPage[schemas.TodoList]:
    if not group_service.is_user_in_group(current_user.id, group_id, db):
        raise HTTPException(403, detail="请先加入此团队")
    query = db.query(models.TodoList).filter(models.TodoList.group_id == group_id)
    count = query.count()
    db_items = query.order_by(desc(models.TodoList.id)).offset((page - 1) * size).limit(size)
    pages = math.ceil(count / size)
    return schemas.AbstractPage[schemas.TodoList](pages=pages, items=db_items)


def create_todo_item(item: schemas.TodoItemCreate, current_user: models.User, db: session) -> models.TodoList:
    if not group_service.is_user_in_group(current_user.id, item.group_id, db):
        raise HTTPException(403, detail="请先加入此团队")
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