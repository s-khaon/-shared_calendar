from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body, Query
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_token_header
from entity import models, schemas
from service import todo_list as todo_service
from service.users import get_current_active_user

router = APIRouter(
    prefix="/api/todo",
    tags=["todo"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/{group_id}/", response_model=list[schemas.TodoItemsGroupByDate], name="代办列表")
async def get_items(group_id: Annotated[int, Path(title="团队id")],
                    from_date: Annotated[str, Query(title="起始日期", regex=r"^\d{4}-\d{2}-\d{2}$")],
                    to_date: Annotated[str, Query(title="截止日期", regex=r"^\d{4}-\d{2}-\d{2}$")],
                    current_user: models.User = Depends(get_current_active_user),
                    db: Session = Depends(get_db)):
    return todo_service.get_todo_list(group_id, current_user, db, from_date, to_date)


@router.get("/{group_id}/undetermined/", response_model=list[schemas.TodoList], name="代办列表")
async def get_undetermined_items(group_id: Annotated[int, Path(title="团队id")],
                                 current_user: models.User = Depends(get_current_active_user),
                                 db: Session = Depends(get_db)):
    return todo_service.get_undetermined_todo_list(group_id, current_user, db)


@router.post("/item/", name="新建待办事项", response_model=schemas.TodoList)
async def create_todo_item(item: Annotated[schemas.TodoItemCreate, Body()],
                           current_user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return todo_service.create_todo_item(item, current_user, db)


@router.put("/item/", response_model=schemas.TodoList, name="修改待办事项")
async def update_todo_item(item: Annotated[schemas.TodoItemUpdate, Body()],
                           current_user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return todo_service.update_todo_item(item, current_user, db)


@router.delete("/item/{item_id}/", response_model=schemas.MSGResponse, name="删除待办事项")
async def update_todo_item(item_id: Annotated[int, Path(title="待办事项id")],
                           current_user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    todo_service.delete_todo_item(item_id, current_user, db)
    return schemas.MSGResponse(detail="删除成功")


@router.put("/item/done/", response_model=schemas.MSGResponse, name="完成代办事项")
async def update_todo_item_done(req: Annotated[schemas.DoneTodoItem, Body(title="完成情况")],
                                current_user: models.User = Depends(get_current_active_user),
                                db: Session = Depends(get_db)):
    todo_service.done_todo_item(req, current_user, db)
    return schemas.MSGResponse()


@router.delete("/item/done/{item_id}/", response_model=schemas.MSGResponse, name="取消完成代办事项")
async def cancel_update_todo_item_done(item_id: Annotated[int, Path(title="待办事项id")],
                                       current_user: models.User = Depends(get_current_active_user),
                                       db: Session = Depends(get_db)):
    todo_service.cancel_todo_item(item_id, current_user, db)
    return schemas.MSGResponse()
