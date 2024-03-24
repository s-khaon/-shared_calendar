from typing import Annotated

from fastapi import HTTPException, Depends, APIRouter, status, Body
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_token_header
from entity import schemas
from entity.schemas import Token, LoginResponse, UserDetail
from service import users as user_service
from service.users import authenticate_user, create_access_token

router = APIRouter(
    prefix="/api",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/users/", response_model=list[schemas.UserPublic], dependencies=[Depends(get_token_header)],
            name="获取用户列表")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.UserPublic, dependencies=[Depends(get_token_header)],
            name="获取用户详情")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/login", name="登录", response_model=LoginResponse)
async def login_for_access_token(
        req: Annotated[schemas.UserLogin, Body()], db: Session = Depends(get_db)
) -> LoginResponse:
    user = authenticate_user(db, req.email, req.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return LoginResponse(token=Token(access_token=access_token, token_type="bearer"),
                         info=UserDetail(email=user.email, nickname=user.nickname, id=user.id, is_active=user.is_active))


@router.post("/register", name="注册", response_model=LoginResponse)
async def register_user(user: Annotated[schemas.UserCreate, Body()], db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="此邮箱已被注册")
    new_one = user_service.create_user(db, user)
    access_token = create_access_token(
        data={"sub": new_one.email}
    )
    return LoginResponse(token=Token(access_token=access_token, token_type="bearer"),
                         info=UserDetail(email=new_one.email, nickname=new_one.nickname, id=new_one.id, is_active=new_one.is_active))
