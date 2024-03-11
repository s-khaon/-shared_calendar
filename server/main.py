from fastapi import FastAPI

from entity import models
from database import engine
from routers import users, groups

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(groups.router)
