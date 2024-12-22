from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from . import models, schemas, utils
from .dependencies import get_db
from .services import auth_services  # 인증 관련 서비스 함수들을 모아둔 파일
from .config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await auth_services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    return await auth_services.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await auth_services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie("access_token") # 쿠키 기반 인증을 사용하는 경우
    return response

@router.post("/token", response_model=schemas.Token)
async def refresh_token():
    # refresh token을 이용하여 access token을 갱신하는 로직
    # (구현은 프로젝트에 따라 다를 수 있습니다.)
    pass