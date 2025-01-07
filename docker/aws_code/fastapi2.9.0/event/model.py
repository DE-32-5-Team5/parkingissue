from pydantic import BaseModel
from typing import Optional

class EventModel(BaseModel):
    c_id: str
    title: str
    address: str
    contact: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: str