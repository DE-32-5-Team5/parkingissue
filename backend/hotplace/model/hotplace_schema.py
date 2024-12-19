from typing import List, Dict, Any
from pydantic import BaseModel, Field, SecretStr 

# {
#   "Contents": {
#     "title": "Sample Title",
#     "address": "123 Main Street, Seoul",
#     "eventstartdate": "2024-12-20T09:00:00",
#     "eventenddate": "2024-12-20T18:00:00",
#     "tel": "010-1234-5678",
#     "firstimage": "https://example.com/thumbnail.jpg",
#     "firstimage2": "https://example.com/image.jpg",
#     "mapx": 126.9784,
#     "mapy": 37.5665,
#     "description": "This is a sample description of the event or place."
#   },
#   "ContentsList": {
#     "title": "Sample Title",
#     "eventstartdate": "2024-12-20T09:00:00",
#     "eventenddate": "2024-12-20T18:00:00",
#     "mapx": 126.9784,
#     "mapy": 37.5665
#   }
# }

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
    firstimage: str = Field(..., description="썸네일 이미지 주소")
    mapx: float = Field(..., description="longitude")
    mapy: float = Field(..., description="latitude")

class RequestHotplaceSchemaq(BaseModel):
    Contents: HotplaceSchema = Field(..., description="게시글 정보")
    ContentsList: HotplaceListSchema = Field(..., description="게시판 정보")