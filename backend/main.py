import uvicorn
from fastapi import FastAPI

from routers import login, register, location, hotplace, mypage
from routers import event

app = FastAPI(docs_url='/api/docs', openapi_url='/api/openapi.json')

app.include_router(login.router)
app.include_router(register.router)
app.include_router(location.router)
app.include_router(hotplace.router)
app.include_router(mypage.router)
app.include_router(event.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)