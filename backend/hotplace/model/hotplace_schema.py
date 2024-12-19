from typing import List, Dict, Any
from pydantic import BaseModel, Field, SecretStr 

# jsonExample = {
#     "User":{
#         "name": "김태영",
#         "nickname": "버블",
#         "id": "kty0904kty",
#         "password": "qwer1234"
#     }
# }

# Field(...)은 꼭 필요한 값임을 나타냄.
# <Class'ellipsis'>

# 게시글 스키마
class HotplaceSchema(BaseModel):
    title: str = Field(..., description="게시글 제목")
    address: str = Field(..., description="게시글 주소")
    eventstartdate: str = Field(..., description="시작 시간")
    eventenddate: str = Field(..., description="끝나는 시간")
    tel: str = Field(..., description="전화번호")
    firstimage: str = Field(..., description="썸네일 이미지 주소")
    firstimage2: str = Field(..., description="게시글 이미지 주소")
    mapx: float = Field(..., description="longitude")
    mapy: float = Field(..., description="latitude")
    description: str = Field(..., description="개요")

# 게시판 스키마
class HotplaceListSchema(BaseModel):
    title: str = Field(..., description="게시글 제목")
    eventstartdate: str = Field(..., description="시작 시간")
    eventenddate: str = Field(..., description="끝나는 시간")
    mapx: float = Field(..., description="longitude")
    mapy: float = Field(..., description="latitude")

class RequestHotplaceSchemaq(BaseModel):
    Contents: HotplaceSchema = Field(..., description="게시글 정보")
    ContentsList: HotplaceListSchema = Field(..., description="게시판 정보")

# jsonExample = {
#     "Manager":{
#         "company": "삼둘샵",
#         "name": "김태영",
#         "phone": "010-1234-5678"
#         "id": "kty0904kty",
#         "password": "qwer1234"
#     }
# }

# 기업회원 스키마
# class ManagerSchema(BaseModel):
#     company: str = Field(..., description="기업의 이름")
#     name: str = Field(..., description="담당자의 이름")
#     phone: SecretStr = Field(..., description="담당자의 번호")
#     id: str = Field(..., description="기업회원의 ID")
#     password: SecretStr = Field(..., description="기업회원의 비밀번호")


# class RequestManagerSchema(BaseModel):
#     Manager: ManagerSchema = Field(..., description="기업회원 정보")