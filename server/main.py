from fastapi import FastAPI

from entity import models
from database import engine
from routers import users, groups, todo_list

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="共享日历",
    description="跨平台团队共享日历、纪念日、代办事项"
)

app.include_router(users.router)
app.include_router(groups.router)
app.include_router(todo_list.router)
