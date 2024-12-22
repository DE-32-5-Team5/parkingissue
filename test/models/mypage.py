from pydantic import BaseModel

# 데이터베이스 모델 import (database.py에 정의된 UserInfo 모델)
from ..database import Base, engine  # Base를 import하고 engine을 사용하여 테이블 생성

# 이전에 작성한 UserInfo 모델을 사용
from .login import UserInfo  

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

Base.metadata.create_all(bind=engine)  # 테이블 생성