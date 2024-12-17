import bcrypt
import os
from jose import jwt
from datetime import datetime, timedelta
from db import get_user_by_id, get_all_users
from models.user_info import UserInfo
from typing import Optional, List

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

async def create_user(user: UserInfo):
    hashed_password = hash_password(user.pw)
    user.pw = hashed_password
    return await create_user(email=user.id, hashed_password=hashed_password, name=user.name)

async def get_user_by_id(id: str) -> Optional[UserInfo]:
    user_data = await get_user_by_id(id=id)
    if user_data:
        return UserInfo(**user_data)  # dict를 pydantic 모델로 변환
    return None

async def get_all_users() -> List[UserInfo]:
    users_data = await get_all_users()
    user_list = []
    if users_data:
        for user_data in users_data:
            user = UserInfo(**user_data)
            user_list.append(user)
    return user_list

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt