from datetime import date, datetime
from pydantic import BaseModel, Field

class FestivalInfo(BaseModel):

    fid: int = Field(..., description="Index")
    title: str = Field(..., description="Festival Title")
    address: str = Field(..., description="Festival Address")
    eventstartdate: date = Field(description="Festival Start Date")
    eventenddate: date = Field(description="Festival End Date")
    tel: str = Field(description="Festival Tel Info")
    firstimage: str = Field(description="Festival Image")
    firstimage2: str = Field(description="Festival Image2")
    mapx: float = Field(description="Festival Location x")
    mapy: float = Field(description="Festival Location y")
    description: str = Field(description="Festival Description")