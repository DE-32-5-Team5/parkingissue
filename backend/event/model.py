from pydantic import BaseModel
from typing import Optional

class EventModel(BaseModel):
    title: str
    address: str
    contact: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: str