from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext

# 데이터베이스 연결 설정
DATABASE_URL = "mysql+pymysql://root:${USER_PASSWORD}@localhost:6033/parkingissue"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy 모델 정의
Base = declarative_base()

class User(Base):
    __tablename__ = "user_info"

    email = Column(String, primary_key=True, index=True)
    pw = Column(String)

# 데이터베이스 세션 가져오기
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 비밀번호 암호화 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# CORS 설정
origins = [
    "http://localhost",  # 필요에 따라 프론트엔드 도메인 추가
    "http://localhost:8080",  # 개발 서버 포트 등
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="로그인 실패")

    if not pwd_context.verify(password, user.pw):
        raise HTTPException(status_code=401, detail="로그인 실패")

    return {"message": "로그인 성공"}

@app.post("/api/signin")
async def signin(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

@app.get("/api/test")
async def test():
    return "ok"

