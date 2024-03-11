from datetime import datetime

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(max_length=100, title="邮箱")
    nickname: str = Field(max_length=20, title="昵称")


class UserCreate(UserBase):
    password: str = Field(max_length=20, title="密码")


class UserLogin(BaseModel):
    email: str = Field(max_length=100, title="邮箱")
    password: str = Field(max_length=20, title="密码")


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserPublic(BaseModel):
    id: int
    is_active: bool
    nickname: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = Field(max_length=100, title="邮箱")


class LoginResponse(BaseModel):
    token: Token
    info: UserBase


class GroupInfo(BaseModel):
    group_name: str = Field(title="团队名称")
    owner_id: int = Field(title="团队所有者")

    owner: User = Field(title="所有者")
    members: list[User] = Field(title="成员列表")

    class Config:
        from_attributes = True


class GroupCreate(BaseModel):
    group_name: str = Field(max_length=20, title="团队名称")


class JoinGroup(BaseModel):
    invitation_link: str = Field(title="邀请链接")


class QuitGroup(BaseModel):
    group_id: int = Field(title="团队id")


class TodoItemCreate(BaseModel):
    group_id: int = Field(title="团队id")
    name: str = Field(title="代办事项名称", max_length=20)
    description: str = Field(title="事件介绍", max_length=500)
    is_all_day: bool = Field(title="是否为全天事件")
    start_time: datetime = Field(title="计划开始时间")
    end_time: datetime = Field(title="计划结束时间")


class TodoItemUpdate(BaseModel):
    id: int = Field(title="代办事项id")
    name: str = Field(title="代办事项名称", max_length=20)
    description: str = Field(title="事件介绍", max_length=500)
    is_all_day: bool = Field(title="是否为全天事件")
    start_time: datetime | None = Field(title="计划开始时间")
    end_time: datetime | None = Field(title="计划结束时间")


class DoneTodoItem(BaseModel):
    id: int = Field(title="代办事项id")
    done_result: str = Field(title="完成结果", max_length=50)
