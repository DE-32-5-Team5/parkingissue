from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from login.routers import user_router, auth_router

app = FastAPI()
app.include_router(user_router.router)

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
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    # TODO: 데이터베이스 또는 다른 인증 방식을 사용하여 사용자 인증
    if email == "test@example.com" and password == "password":
        return {"message": "로그인 성공"}
    else:
        raise HTTPException(status_code=401, detail="로그인 실패")