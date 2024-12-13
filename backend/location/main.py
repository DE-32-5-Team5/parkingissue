from fastapi import FastAPI, HTTPException
from model import Location, FromSpark
from kafka_producer import send_to_kafka
import requests


app = FastAPI(docs_url='/api/docs', openapi_url='/api/openapi.json')

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/api/location")
async def create_item(location: Location):
    return "hello"
    #send_to_kafka({"lo": location.lo, "la": location.la})
    #return {"lo": location.lo, "la": location.la}

#스파크에서 id, lo, la가 json형식으로 올 거임. 그걸 받아서 다시 front에 post형식으로 보내기
stored_data={}
@app.post("/api/getlocation")
async def receive_location(sparkdata: FromSpark):
    print(f"Received location: {sparkdata}")
    if not sparkdata:
        raise HTTPException(status_code=400, detail="Empty JSON data")

    stored_data.clear()
    stored_data.update(sparkdata)
    return {"message": "Data received and stored successfully.", "stored_data": stored_data}




#프론트에서 get요청 보내면 데이터 보내주는 부분
@app.get("/api/frontget/")
async def frontget():
    if not stored_data:
        return {"message": "데이터가 없습니다."}

    return {"stored_data": stored_data}
