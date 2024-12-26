from typing import List, Dict, Any
from pydantic import BaseModel, Field, SecretStr 

# {
#   "BookmarkList": {
#     "title": "Sample Title",
#     "mapx": 126.9784,
#     "mapy": 37.5665
#   }
# }

# 북마크 스키마
class BookmarkListSchema(BaseModel):
    title: str = Field(..., description="북마크 제목")
    idtype: SecretStr = Field(..., description="로그인 타입")
    idcode: SecretStr = Field(..., description="id")
    mapx: float = Field(..., description="longitude")
    mapy: float = Field(..., description="latitude")

class BookmarkCreationSchema(BaseModel):
    idtype: SecretStr = Field(..., description="로그인 타입")
    idcode: SecretStr = Field(..., description="id")
    contentid: str = Field(..., description="컨텐츠 아이디")
    bookmark_nickname: str = Field(..., description="북마크 닉네임")

class BookmarkCheckSchema(BaseModel):
    idtype: SecretStr = Field(..., description="로그인 타입")
    idcode: SecretStr = Field(..., description="id")
    contentid: str = Field(..., description="컨텐츠 아이디")

class BookmarkDeleteSchema(BaseModel):
    idtype: SecretStr = Field(..., description="로그인 타입")
    idcode: SecretStr = Field(..., description="id")
    contentid: str = Field(..., description="컨텐츠 아이디")

class BookmarkUpdateSchema(BaseModel):
    idtype: SecretStr = Field(..., description="로그인 타입")
    idcode: SecretStr = Field(..., description="id")
    contentid: str = Field(..., description="컨텐츠 아이디")
    bookmark_nickname: str = Field(..., description="북마크 닉네임")

class RequestBookmarkSchema(BaseModel):
    ContentsList: BookmarkListSchema = Field(..., description="북마크 정보")
    BookmarkCreation: BookmarkCreationSchema = Field(..., description="북마크 등록")
    BookmarkCheck: BookmarkCheckSchema = Field(..., description="북마크 여부 체크")
    BookmarkDelete: BookmarkDeleteSchema = Field(..., description="북마크 삭제")
    BookmarkUpdate: BookmarkUpdateSchema = Field(..., description="북마크 수정")