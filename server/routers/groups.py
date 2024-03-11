from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_token_header
from entity import models, schemas
from service import groups as group_service
from service.users import get_current_active_user

router = APIRouter(
    prefix="/api/groups",
    tags=["groups"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/", description="创建团队", response_model=schemas.GroupInfo)
async def create_group(group: Annotated[schemas.GroupCreate, Body()], db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_active_user)):
    return group_service.create_group(db, group, current_user)


# todo 完成邀请和加入逻辑