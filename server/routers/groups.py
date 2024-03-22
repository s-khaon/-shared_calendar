from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path, Query
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


@router.post("/", name="创建团队", response_model=schemas.GroupInfo)
async def create_group(group: Annotated[schemas.GroupCreate, Body()], db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_active_user)):
    return group_service.create_group(group, current_user, db)


@router.put("/", name="更新团队", response_model=schemas.GroupInfo)
async def create_group(group: Annotated[schemas.GroupUpdate, Body()], db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_active_user)):
    return group_service.update_group(group, current_user, db)


@router.get("/", response_model=list[schemas.GroupInfo], name="团队列表")
async def get_groups(current_user: models.User = Depends(get_current_active_user)):
    return group_service.get_groups(current_user)


@router.get("/{group_id}/", response_model=schemas.GroupInfo, name="团队详情")
async def get_group(group_id: Annotated[int, Path(title="团队id")], db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_active_user)):
    return group_service.get_group_detail(group_id, current_user, db)


@router.delete("/{group_id}/member/quit/", name="退出团队")
async def quit_group(group_id: Annotated[int, Path(title="团队id")], db: Session = Depends(get_db),
                     current_user: models.User = Depends(get_current_active_user)) -> None:
    group_service.quit_group(group_id, current_user, db)


@router.delete("/{group_id}/", name="删除团队")
async def delete_group(group_id: Annotated[int, Path(title="团队id")], db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_active_user)) -> None:
    group_service.delete_group(group_id, current_user, db)


@router.post("/invitation/{group_id}/", name="生成邀请码", response_model=schemas.JoinGroup)
async def create_group_invitation_code(group_id: Annotated[int, Path(title="团队id")], db: Session = Depends(get_db),
                                       current_user: models.User = Depends(get_current_active_user)):
    return group_service.create_invitation_code(group_id, current_user, db)


@router.get("/invitation/{code}/", name="邀请详情", response_model=schemas.InvitationInfo)
async def invitation_detail(code: Annotated[str, Path(title="邀请码")], db: Session = Depends(get_db)):
    return group_service.get_invitation_info(code, db)


@router.post("/member/join/", name="加入团队", response_model=schemas.MSGResponse)
async def join_group(code: Annotated[str, Query(title="邀请码")], db: Session = Depends(get_db),
                     current_user: models.User = Depends(get_current_active_user)):
    group_service.join_group(code, current_user, db)
    return schemas.MSGResponse(detail="加入成功")
