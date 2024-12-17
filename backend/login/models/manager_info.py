from typing import Optional
from pydantic import BaseModel

class UserInfo(BaseModel):
    id: Optional[str] = None
    pw: Optional[str] = None
    name: str