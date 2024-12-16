from pydantic import BaseModel

class Location(BaseModel):
    lo: float
    la: float


class FromSpark(BaseModel):
    parkid: str
    parknm: str
    parkaddr: str
    lo: float
    la: float
