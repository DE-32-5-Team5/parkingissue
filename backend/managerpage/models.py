from sqlalchemy import Column, Integer, String
from .database import Base

class ManagerInfo(Base):
    __tablename__ = 'manager_info'

    managerid = Column(Integer, primary_key=True, index=True)  # 'userid'를 'managerid'로 변경
    nickname = Column(String, index=True)
    password = Column(String)