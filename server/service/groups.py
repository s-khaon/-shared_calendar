import datetime
import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from entity import schemas, models


def create_group(group: schemas.GroupCreate, user: models.User, db: Session) -> models.Group:
    db_group = models.Group(group_name=group.group_name, owner_id=user.id)
    db_group.members.append(user)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def update_group(group: schemas.GroupUpdate, user: models.User, db: Session) -> models.Group:
    db_group = get_group_by_id(group.id, db)
    if not db_group:
        raise HTTPException(404, "团队不存在")
    if db_group.owner_id != user.id:
        raise HTTPException(403, "您不是团队所有者，无法修改")
    db_group.group_name = group.group_name
    db.commit()
    return db_group


def get_groups(user: models.User):
    return user.groups


def get_group_by_id(group_id: int, db: Session):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def get_group_detail(group_id: int, user: models.User, db: Session):
    db_group = get_group_by_id(group_id, db)
    if not db_group:
        raise HTTPException(404, "团队不存在")
    for member in db_group.members:
        if member.id == user.id:
            return db_group
    else:
        raise HTTPException(403, "请先加入团队")


def quit_group(group_id: int, user: models.User, db: Session):
    db_group = get_group_by_id(group_id, db)
    if not db_group:
        raise HTTPException(404, "团队不存在")
    if db_group.owner_id == user.id:
        raise HTTPException(403, "团队所有者无法退出，如需退出请删除团队")
    db_group.members.remove(user)
    db.commit()


def delete_group(group_id: int, user: models.User, db: Session):
    db_group = get_group_by_id(group_id, db)
    if db_group and db_group.owner_id == user.id:
        db.delete(db_group)
        db.commit()


def create_invitation_code(group_id: int, user: models.User, db: Session) -> str:
    db_group = get_group_by_id(group_id, db)
    if db_group and db_group.owner_id == user.id:
        db_code = models.GroupInvitation(group_id=group_id, code=uuid.uuid4().hex, creator_id=user.id)
        db.add(db_code)
        db.commit()
        return db_code
    else:
        raise HTTPException(status_code=403, detail="只能团队所有者邀请成员")


# 通过邀请码获取邀请详情
def get_invitation_info(code: str, db: Session):
    db_code = db.query(models.GroupInvitation).filter_by(code=code).first()
    if not db_code:
        raise HTTPException(status_code=404, detail="邀请链接不存在")
    return db_code


def is_user_in_group(user_id: int, group_id: int, db: Session) -> bool:
    return db.query(models.group_users).filter_by(group_id=group_id, user_id=user_id).scalar()


def join_group(code: str, user: models.User, db: Session):
    invitation_record: models.GroupInvitation = db.query(models.GroupInvitation).filter(
        models.GroupInvitation.code == code).first()
    if not invitation_record:
        raise HTTPException(status_code=404, detail="邀请链接不存在")
    if invitation_record.joined_at is not None:
        raise HTTPException(status_code=400, detail="此邀请码已被使用")
    if is_user_in_group(user.id, invitation_record.group_id, db):
        raise HTTPException(status_code=400, detail="请勿重复加入")
    invitation_record.joined_at = datetime.datetime.now()
    db_group = get_group_by_id(invitation_record.group_id, db)
    if not db_group:
        raise HTTPException(status_code=404, detail="此团队不存在")
    db_group.members.append(user)
    db.commit()
