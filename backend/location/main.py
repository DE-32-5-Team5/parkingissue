from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from model import Location, FromSpark, Getdf, RequestBody
from kafka_producer import send_to_kafka
import requests
from typing import List


app = FastAPI(docs_url='/api/docs', openapi_url='/api/openapi.json')

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/api/location")
async def create_item(location: Location):
    #return "hello"
    print(location)
    send_to_kafka({"latitude": str(location.latitude), "longitude": str(location.longitude)})
    return {"latitude": str(location.latitude), "longitude": str(location.longitude)}

stored_data = []
#스파크에서 id, lo, la가 json형식으로 올 거임. 그걸 받아서 다시 front에 post형식으로 보내기
@app.post("/api/getlocation")
async def receive_location(sparkdata: List[FromSpark]):
    # 데이터가 한줄씩 들어오고 있음
    #print(f"Received location: {sparkdata}")
    global stored_data
    if not sparkdata:
        raise HTTPException(status_code=400, detail="Empty JSON data")
    # 초기화
    stored_data = []
    # 값 추가
    stored_data.extend(sparkdata)
    #print(stored_data)
    return {"message": "Data received and stored successfully.", "stored_data": stored_data}

#프론트에서 get요청 보내면 데이터 보내주는 부분
@app.get("/api/frontget/")
async def frontget():
    if not stored_data:
        return {"message": "데이터가 없습니다."}
    #print(stored_data)
    encoded_data = jsonable_encoder(stored_data)
    response = JSONResponse(content={"stored_data": encoded_data})
    response.headers["Cache-Control"] = "no-store"
    return response
