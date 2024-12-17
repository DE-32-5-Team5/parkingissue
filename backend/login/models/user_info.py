from typing import Optional
from pydantic import BaseModel

class UserInfoBase(BaseModel):
    id: str
    name: str
    naver_id: Optional[str] = None
    kakao_id: Optional[str] = None

class UserInfoCreate(UserInfoBase):
    pw: str

class UserInfo(UserInfoBase):
    pw: Optional[str] = None

    class Config:
        orm_mode = True