import bcrypt
import os
from jose import jwt
from datetime import datetime, timedelta
from db import get_manager_by_id, get_all_managers, create_manager  # db.py 에서 구현 필요
from models.manager_info import ManagerInfo  # UserInfo -> ManagerInfo
from typing import Optional, List

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
  return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

async def create_manager(manager: ManagerInfo):
  hashed_password = hash_password(manager.pw)
  manager.pw = hashed_password
  # manager_info 테이블에 맞게 데이터 저장 (db.py 에서 구현)
  return await create_manager(data=manager.dict())  # pydantic model -> dict

async def get_manager_by_id(id: str) -> Optional[ManagerInfo]:
  manager_data = await get_manager_by_id(id=id)  # get_user_by_id -> get_manager_by_id
  if manager_data:
    return ManagerInfo(**manager_data)  # dict를 pydantic 모델로 변환
  return None

async def get_all_managers() -> List[ManagerInfo]:
  managers_data = await get_all_managers()  # get_all_users -> get_all_managers
  manager_list = []
  if managers_data:
    for manager_data in managers_data:
      manager = ManagerInfo(**manager_data)
      manager_list.append(manager)
  return manager_list

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt