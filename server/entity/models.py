from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Table, JSON, Date

from database import Base

from sqlalchemy.orm import relationship


class ModelBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, comment="记录id")
    created_at = Column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, nullable=False, comment="修改时间")


group_users = Table(
    "group_users",
    Base.metadata,
    Column("group_id", Integer, nullable=False, primary_key=True, comment="团队id"),
    Column("user_id", Integer, nullable=False, primary_key=True, comment="用户id"),
    Column("created_at", DateTime, default=datetime.now, nullable=False, comment="创建时间")
)


class User(ModelBase):
    __tablename__ = "users"

    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    nickname = Column(String(20), comment="用户昵称", nullable=False, default="")
    hashed_password = Column(String(200), comment="加密后密码")
    is_active = Column(Boolean, default=True, comment="是否激活")
    groups = relationship(
        "Group",
        back_populates="members",
        secondary=group_users,
        primaryjoin="User.id == group_users.c.user_id",
        secondaryjoin="Group.id == group_users.c.group_id",
        # remote_side=[group_users.c.user_id],
    )


class Group(ModelBase):
    __tablename__ = "groups"

    group_name = Column(String(20), index=True, nullable=False, comment="团队名称")
    owner_id = Column(Integer, nullable=False, comment="团队所有者")

    todo_items = relationship("TodoList", back_populates="group", primaryjoin="foreign(TodoList.group_id) == Group.id",
                              cascade="all, delete")

    owner = relationship("User", primaryjoin="foreign(Group.owner_id) == User.id")
    members = relationship(
        "User",
        secondary=group_users,
        back_populates="groups",
        primaryjoin="group_users.c.group_id == Group.id",
        secondaryjoin="group_users.c.user_id == User.id"
    )


class GroupInvitation(ModelBase):
    __tablename__ = "group_invitations"

    group_id = Column(Integer, nullable=False, comment="所属团队")
    creator_id = Column(Integer, nullable=False, comment="创建人")
    code = Column(String(36), nullable=False, comment="链接")
    joined_at = Column(DateTime, nullable=True, comment="加入时间")

    group = relationship("Group", primaryjoin="foreign(GroupInvitation.group_id) == Group.id")
    creator = relationship("User", primaryjoin="foreign(GroupInvitation.creator_id) == User.id")


class TodoList(ModelBase):
    __tablename__ = "todo_list"

    group_id = Column(Integer, nullable=False, comment="所属团队")
    user_id = Column(Integer, nullable=False, comment="创建人")
    name = Column(String(20), nullable=False, comment="代办事项名称")
    description = Column(String(500), nullable=False, default="", comment="事件介绍")
    done_time = Column(DateTime, nullable=True, comment="完成时间")
    done_by = Column(Integer, nullable=True, comment="完成人")
    done_result = Column(String(50), nullable=True, default="", comment="完成结果")
    is_all_day = Column(Boolean, default=False, comment="全天事件", nullable=False)
    start_time = Column(DateTime, nullable=False, comment="计划开始时间")
    end_time = Column(DateTime, nullable=True, comment="计划结束时间")

    group = relationship("Group", primaryjoin="foreign(TodoList.group_id) == Group.id", back_populates="todo_items")
    done_user = relationship("User", primaryjoin="foreign(TodoList.done_by) == User.id")
    creator = relationship("User", primaryjoin="foreign(TodoList.user_id) == User.id")

    @property
    def is_done(self) -> bool:
        return True if self.done_time else False

    @is_done.setter
    def is_done(self, value: bool) -> None:
        if value:
            self.done_time = datetime.now()
        else:
            self.done_time = None


class Holiday(ModelBase):
    __tablename__ = "holidays"
    name = Column(String(10), nullable=False, comment="节假日名称")
    start_date = Column(Date, nullable=False, comment="开始日期")
    end_date = Column(Date, nullable=False, comment="结束日期")
    comp_days = Column(JSON, nullable=False, default=[], comment="补班日期")
    memo = Column(String(100), nullable=False, default="", comment="备注")
