from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_token_header, get_page_query
from entity import models, schemas
from service import todo_list as todo_service
from service.users import get_current_active_user

router = APIRouter(
    prefix="/api/todo",
    tags=["todo"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/{group_id}/", response_model=schemas.AbstractPage[schemas.TodoList], name="代办列表")
async def get_groups(group_id: Annotated[int, Path(title="团队id")],
                     page_query: schemas.PageQuery = Depends(get_page_query),
                     current_user: models.User = Depends(get_current_active_user),
                     db: Session = Depends(get_db)):
    return todo_service.get_todo_list(group_id, current_user, db, page_query.page, page_query.size)


@router.post("/item", name="新建待办事项", response_model=schemas.TodoList)
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
