import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from routers.login import r_login
from routers.register import r_register
from routers.location import r_location
from routers.hotplace import r_hotplace
from routers.mypage import r_mypage
from routers.event import r_event

app = FastAPI(docs_url='/api/docs', openapi_url='/api/openapi.json')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인을 허용하려면 ["*"]
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

app.include_router(r_login)
app.include_router(r_register)
app.include_router(r_location)
app.include_router(r_hotplace)
app.include_router(r_mypage)
app.include_router(r_event)

@app.get('/')
def home():
    return {'Mag' : 'Main'}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)