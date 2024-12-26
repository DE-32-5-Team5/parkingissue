from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from location.model import Location, FromSpark, Getdf, RequestBody
from location.pymysql_module import select_park_info, related_data
from location.kafka_producer import send_to_kafka
import requests
from typing import List

# 유저, 기업 정보 스키마
from register.model.register_schema import RequestUserSchema, UserSchema, RequestManagerSchema, ManagerSchema
# pip install "passlib[bcrypt]"
from passlib.context import CryptContext

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
        stored_data = []
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

@app.get("/api/getParkInfo")
async def get_park_info(parkid: str):
    try:
        park_info = select_park_info(parkid)
        if not park_info:
            raise HTTPException(status_code=404, detail="Park not found")
        print(park_info)
        return park_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/getRelated")
async def get_related_data(text: str):
    # [{'park_nm': '무궁화주차빌딩'}, {'park_nm': '무궁화빌라'}, {'park_nm': '무궁화타운 제3동'}, {'park_nm': '무궁화타운 제4 동'}, {'park_nm': '무궁화타운 제5동'}]
    result = related_data(text)
    if result:
        dic = {}
        for i in result:
            for key, value in i.items():
                if key not in dic:
                    dic[key] = [value]
                else:
                    dic[key].append(value)
        print(dic)
    return result

# 검색어 로그 to Kafka
@app.get("/api/getClickSearch")
async def get_click_search(txt: str):
    send_to_kafka2({'search_msg' : txt})
    print('연관검색어 카프카 전송 완료')
    return {'search_msg' : txt}

# 회원가입 폼 - ID 체크 / 개인
@app.post("/api/users/check")
async def user_check_id(request: RequestUserSchema):
    from register.modules.user_register import check_user_id, insert_user_info

    user_id = request.User.id  # 올바르게 ID를 추출
    if not check_user_id(user_id):  # ID 중복 확인
        raise HTTPException(status_code=400, detail="user_id isn't Unique")
    
    # ID가 고유하다면 성공 상태를 반환
    return JSONResponse(content={"status": 200, "detail": "user_id is Unique"}, status_code=200)

# 회원가입 폼 - ID 체크 / 기업
@app.post("/api/company/check/id")
async def manager_check_id(request: RequestManagerSchema):
    from register.modules.manager_register import check_manager_id, insert_manager_info

    manager_id = request.Manager.id  # 올바르게 ID를 추출
    if not check_manager_id(manager_id):  # ID 중복 확인
        raise HTTPException(status_code=400, detail="manager_id isn't Unique")
    
    # ID가 고유하다면 성공 상태를 반환
    return JSONResponse(content={"status": 200, "detail": "manager_id is Unique"}, status_code=200)

# 회원가입 폼 - 전화번호 체크 / 기업
@app.post("/api/company/check/phone")
async def user_register(request: RequestManagerSchema):
    from register.modules.manager_register import check_manager_phone, insert_manager_info

    manager_phone = request.Manager.phone  # 올바르게 phone를 추출
    if not check_manager_phone(manager_phone):  # phone 중복 확인
        raise HTTPException(status_code=400, detail="manager_phone isn't Unique")
    
    # ID가 고유하다면 성공 상태를 반환
    return JSONResponse(content={"status": 200, "detail": "manager_phone is Unique"}, status_code=200)


# 해시 알고리즘 컨텍스트를 생성.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# 회원가입 폼 - 저장 / 개인
@app.post("/api/users/register")
async def user_register(request: RequestUserSchema):
    from register.modules.user_register import check_user_id, insert_user_info

    user_name = request.User.name
    user_nick = request.User.nickname
    user_id = request.User.id  # 올바르게 ID를 추출
    user_pw = get_password_hash(request.User.password) # 해시처리
    
    if not check_user_id(user_id):  # ID 중복 확인
        raise HTTPException(status_code=400, detail="user_id isn't Unique")
    
    # ID가 고유하다면 성공 상태를 반환, 가입
    # db 연결이 원활하지 않으면 에러.
    if insert_user_info(user_name, user_nick, user_id, user_pw): # True
        return JSONResponse(content={"status": 200, "detail": "user registering is success"}, status_code=200)
    return JSONResponse(content={"status": 404, "detail": "user registering is failed"}, status_code=404)

# 회원가입 폼 - 저장 / 기업
@app.post("/api/company/register")
async def manager_check_id(request: RequestManagerSchema):
    from register.modules.manager_register import check_manager_id, insert_manager_info

    manager_company = request.Manager.company
    manager_name = request.Manager.name
    manager_phone = request.Manager.phone
    manager_id = request.Manager.id # 올바르게 ID를 추출
    manager_password = get_password_hash(request.Manager.password) # 해시처리

    if not check_manager_id(manager_id):  # ID 중복 확인
        raise HTTPException(status_code=400, detail="manager_id isn't Unique")
    
    # ID가 고유하다면 성공 상태를 반환. 가입
    # db 연결이 원활하지 않으면 에러.
    if insert_manager_info(manager_company, manager_name, manager_phone, manager_id, manager_password):
        return JSONResponse(content={"status": 200, "detail": "manager_id is Unique"}, status_code=200)
    return JSONResponse(content={"status": 404, "detail": "company registering is failed"}, status_code=404)
