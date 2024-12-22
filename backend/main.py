from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import login, register, location, hotplace, mypage
from .routers import event

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

app.include_router(login.router)
app.include_router(register.router)
app.include_router(location.router)
app.include_router(hotplace.router)
app.include_router(mypage.router)
app.include_router(event.router)