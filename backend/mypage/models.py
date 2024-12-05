from sqlalchemy import Column, Integer, String
from .database import Base

class UserInfo(Base):
    __tablename__ = 'user_info'

    userid = Column(Integer, primary_key=True, index=True)  # id -> userid로 변경
    nickname = Column(String, index=True)
    password = Column(String)
    naver_id = Column(String, nullable=True)
    kakao_id = Column(String, nullable=True)
