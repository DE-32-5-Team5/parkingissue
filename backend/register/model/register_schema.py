from typing import List, Dict, Any
from pydantic import BaseModel, Field, SecretStr

# 사용자 스키마
class UserSchema(BaseModel):
    userName: str = Field(..., description="사용자의 이름")
    userNick: str = Field(..., description="사용자의 닉네임")
    userId: str = Field(..., description="사용자의 ID")
    userPw: str = Field(..., description="사용자의 비밀번호")


class RequestUserSchema(BaseModel):
    User: UserSchema = Field(..., description="사용자 정보")

# 중복체크용 스키마
class CheckSchema(BaseModel):
    id: str = Field(...)

# 기업회원 스키마
class ManagerSchema(BaseModel):
    company: str = Field(..., description="기업의 이름")
    name: str = Field(..., description="담당자의 이름")
    phone: str = Field(..., description="담당자의 번호")
    companyid: str = Field(..., description="기업회원의 ID")
    password: str = Field(..., description="기업회원의 비밀번호")


class RequestManagerSchema(BaseModel):
    Manager: ManagerSchema = Field(..., description="기업회원 정보")