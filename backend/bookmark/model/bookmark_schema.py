from typing import List, Dict, Any
from pydantic import BaseModel, Field, SecretStr

# 북마크 스키마

#{
#    "contentid": "152433"
#}

class RequestBookmarkSchema(BaseModel):
    contentid: str = Field(..., description="컨텐츠 아이디")