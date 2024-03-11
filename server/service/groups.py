import datetime
import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from config.config import Config
from entity import schemas, models


def create_group(db: Session, group: schemas.GroupCreate, user: models.User):
    db_group = models.Group(group_name=group.group_name, owner_id=user.id)
    db_group.members.append(user)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_groups(user: models.User):
    return user.groups


def get_group_by_id(group_id: int, db: Session):
    return db.query(models.Group).filter(models.Group.id == group_id).one()


def quit_group(group_id: int, user: models.User, db: Session):
    db_group = get_group_by_id(group_id, db)
    if db_group:
        db_group.members.remove(user)


def delete_group(group_id: int, user: models.User, db: Session):
    db_group = get_group_by_id(group_id, db)
    if db_group and db_group.owner_id == user.id:
        db.delete(db_group)
        db.commit()


def create_invitation_link(group_id: int, user: models.User, db: Session):
    db_group = get_group_by_id(group_id, db)
    if db_group and db_group.owner_id == user.id:
        link = Config.host + "/group/invitation/" + uuid.uuid4().hex
        db_link = models.GroupInvitation(group_id=group_id, link=link, creator_id=user.id)
        db.add(db_link)
        db.commit()
        return link
    else:
        raise HTTPException(status_code=400, detail="只能团队所有者邀请成员")


def join_group(link: str, user: models.User, db: Session):
    # todo 处理重复加入
    invitation_link: models.GroupInvitation = db.query(models.GroupInvitation).filter(models.GroupInvitation.link == link).one()
    if not invitation_link:
        raise HTTPException(status_code=404, detail="邀请链接不存在")
    invitation_link.update_at = datetime.datetime.now()
    db_group = get_group_by_id(invitation_link.group_id, db)
    if not db_group:
        raise HTTPException(status_code=404, detail="此团队不存在")
    db_group.members.append(user)
    db.commit()
