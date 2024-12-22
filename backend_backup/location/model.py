from typing import List, Dict, Any
from pydantic import BaseModel, Field
class Location(BaseModel):
    latitude: float
    longitude: float


class FromSpark(BaseModel):
    park_id: str
    park_nm: str
    park_addr: str
    park_lo: float
    park_la: float
    distance: float

class Getdf(BaseModel):
    detail: List[FromSpark]


class InputData(BaseModel):
    park_id: Dict[str, str]
    park_nm: Dict[str, str]
    park_addr: Dict[str, str]
    park_lo: Dict[str, float]
    park_la: Dict[str, float]
    distance: Dict[str, float]

class DetailItem(BaseModel):
    type: str
    loc: List[str]
    msg: str
    input: Dict[str, Any]  # 변경


class RequestBody(BaseModel):
    detail: List[Dict[str, Any]]