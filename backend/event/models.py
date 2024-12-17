from sqlalchemy import Column, String, Date, Float, BigInteger
from .database import Base

class FestivalInfo(Base):
    __tablename__ = "fastival_info"

    fid = Column(BigInteger, primary_key=True, index=True, autoincrement=True)  # auto_increment 설정
    title = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    eventstartdate = Column(Date, nullable=False)
    eventenddate = Column(Date, nullable=False)
    tel = Column(String(255), nullable=False)
    firstimage = Column(String(255), nullable=False)
    firstimage2 = Column(String(255), nullable=False)
    mapx = Column(Float, nullable=False)
    mapy = Column(Float, nullable=False)
