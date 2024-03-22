from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel, Field, ConfigDict, EmailStr, computed_field
from typing import Generic

T = TypeVar("T")


class SchemasBase(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
    )


class MSGResponse(SchemasBase):
    detail: str = "成功"


class AbstractPage(SchemasBase, Generic[T]):
    pages: int
    items: list[T] | None = []


class PageQuery(SchemasBase):
    page: int = Field(gt=0)
    size: int = Field(gt=0, le=99)


class UserBase(SchemasBase):
    email: str = Field(max_length=100, title="邮箱")
    nickname: str = Field(max_length=20, title="昵称")


class UserDetail(UserBase):
    id: int
    is_active: bool


class UserCreate(UserBase):
    password: str = Field(max_length=20, title="密码")


class UserLogin(SchemasBase):
    email: EmailStr = Field(max_length=100, title="邮箱")
    password: str = Field(max_length=20, title="密码")


class User(UserBase):
    is_active: bool


class UserPublic(SchemasBase):
    id: int
    is_active: bool
    nickname: str


class Token(SchemasBase):
    access_token: str
    token_type: str


class TokenData(SchemasBase):
    email: str = Field(max_length=100, title="邮箱")


class LoginResponse(SchemasBase):
    token: Token
    info: UserDetail


class GroupInfo(SchemasBase):
    id: int = Field(title="团队id")
    group_name: str = Field(title="团队名称")
    owner_id: int = Field(title="团队所有者")

    owner: User = Field(title="创建者")
    members: list[User] = Field(title="成员列表")

    class Config:
        from_attributes = True


class InvitationInfo(SchemasBase):
    code: str = Field(title="邀请码")
    creator_id: int = Field(title="邀请人id")
    group_id: int = Field(title="团队id")

    owner: UserPublic = Field(title="所有者")
    group: GroupInfo = Field(title="团队信息")

    class Config:
        from_attributes = True


class GroupCreate(SchemasBase):
    group_name: str = Field(max_length=20, title="团队名称")


class GroupUpdate(GroupCreate):
    id: int = Field(title="团队id")


class JoinGroup(SchemasBase):
    code: str = Field(title="邀请码")


class QuitGroup(SchemasBase):
    group_id: int = Field(title="团队id")


class TodoItemCreate(SchemasBase):
    group_id: int = Field(title="团队id")
    name: str = Field(title="代办事项名称", max_length=20)
    description: str = Field(title="事件介绍", max_length=500)
    is_all_day: bool = Field(title="是否为全天事件")
    start_time: datetime = Field(title="计划开始时间")
    end_time: datetime | None = Field(title="计划结束时间")


class TodoItemUpdate(SchemasBase):
    id: int = Field(title="代办事项id")
    name: str = Field(title="代办事项名称", max_length=20)
    description: str = Field(title="事件介绍", max_length=500)
    is_all_day: bool = Field(title="是否为全天事件")
    start_time: datetime | None = Field(title="计划开始时间")
    end_time: datetime | None = Field(title="计划结束时间")

    class Config:
        from_attributes = True


class DoneTodoItem(SchemasBase):
    id: int = Field(title="代办事项id")
    done_result: str = Field(title="完成结果", max_length=50)


class TodoList(SchemasBase):
    id: int = Field(title="记录id")
    group_id: int = Field(gt=0, title="所属团队")
    user_id: int = Field(gt=0, title="创建人")
    name: str = Field(max_length=20, title="代办事项名称")
    description: str = Field(max_length=500, default="", title="事件介绍")
    done_time: datetime | None = Field(title="完成时间")
    done_by: int | None = Field(gt=0, title="完成人")
    done_result: str | None = Field(max_length=50, title="完成结果")
    is_all_day: bool = Field(title="全天事件")
    start_time: datetime = Field(title="计划开始时间")
    end_time: datetime | None = Field(title="计划结束时间")
    created_at: datetime = Field(title="创建时间")
    updated_at: datetime = Field(title="修改时间")

    done_user: UserPublic | None = Field(title="完成者")
    creator: UserPublic = Field(title="创建者")

    class Config:
        from_attributes = True

    @computed_field
    @property
    def is_done(self) -> bool:
        return True if self.done_time else False

    @is_done.setter
    def is_done(self, value: bool) -> None:
        if value:
            self.done_time = datetime.now()
        else:
            self.done_time = None


class TodoItemsGroupByDate(SchemasBase):
    key: str
    value: list[TodoList]
