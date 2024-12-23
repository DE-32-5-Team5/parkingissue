from typing import List, Dict, Any
from pydantic import BaseModel, Field, SecretStr 

# {
#   "BookmarkList": {
#     "title": "Sample Title",
#     "mapx": 126.9784,
#     "mapy": 37.5665
#   }
# }

# 게시판 스키마
class BookmarkListSchema(BaseModel):
    title: str = Field(..., description="북마크 제목")
    idtype: SecretStr = Field(..., description="로그인 타입")
    idcode: SecretStr = Field(..., description="id")
    mapx: float = Field(..., description="longitude")
    mapy: float = Field(..., description="latitude")

class RequestBookmarkSchema(BaseModel):
    ContentsList: BookmarkListSchema = Field(..., description="북마크 정보")