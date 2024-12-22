from fastapi import FastAPI, Form, File, UploadFile,HTTPException,Query
import os
import json
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi.responses import JSONResponse
from model import EventModel
from event_db import insert_event_info,get_event_info,get_event_info_by_id
from fastapi.staticfiles import StaticFiles

app = FastAPI(docs_url='/api2/docs', openapi_url='/api2/openapi.json')

# CORS 설정 활성화 - 프론트랑 백엔드 포트가 달라서 브라우저가 막아놓음
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# 업로드 디렉토리 설정
UPLOAD_DIR = os.path.abspath("./uploads")  # 현재 디렉토리 기준으로 업로드 디렉토리 생성
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 정적 파일 경로 설정
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# 이벤트 등록 엔드포인트
@app.post("/api2/event-registration/")
async def register_event(
    event_data: str = Form(...), 
    main_image: UploadFile = File(...),
    thumbnail_image: UploadFile = File(...)
):
    try:
        print(f"Raw event_data: {event_data}") 
        parsed_event_data = json.loads(event_data)
        event = EventModel(**parsed_event_data)  # Pydantic 유효성 검사
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid event_data format: {str(e)}")

    # 파일 저장 경로 생성 (절대 경로)
    main_image_path = os.path.abspath(os.path.join(UPLOAD_DIR, main_image.filename))
    thumbnail_image_path = os.path.abspath(os.path.join(UPLOAD_DIR, thumbnail_image.filename))

    # 파일 저장
    with open(main_image_path, "wb") as buffer:
        buffer.write(await main_image.read())
    with open(thumbnail_image_path, "wb") as buffer:
        buffer.write(await thumbnail_image.read())

    # 파일 URL 생성 (정적 파일 경로)
    main_image_url = f"http://127.0.0.1:8000/uploads/{main_image.filename}"
    thumbnail_image_url = f"http://127.0.0.1:8000/uploads/{thumbnail_image.filename}"

    print(f"Main Image URL: {main_image_url}")
    print(f"Thumbnail Image URL: {thumbnail_image_url}")

    # 데이터베이스에 저장
    if insert_event_info(
        event.title, event.address, event.contact, 
        event.start_date, event.end_date, 
        main_image_url, thumbnail_image_url, event.description
    ): 
        return JSONResponse(
            content={
                "status": 200, 
                "detail": "행사 등록이 완료되었습니다.",
                "main_image_url": main_image_url,
                "thumbnail_image_url": thumbnail_image_url
            },
            status_code=200
        )

    return JSONResponse(content={"status": 404, "detail": "행사 등록에 실패했습니다."}, status_code=404)


    
@app.get("/api2/events")
async def get_event(ID: Optional[str] = Query(None)):
    # ID 값 확인
    if not ID:
        return {"error": "ID가 전달되지 않았습니다."}

    # ID를 사용한 데이터 필터링
    results = get_event_info(ID)  # ID를 기반으로 데이터베이스 조회 함수
    print(results)
    if not results:
        return {"error": f"ID {ID}에 해당하는 이벤트가 없습니다."}

    return {"id": ID, "events": results}

# 이벤트 카드 클릭했을 때
@app.get("/api2/event-details/")
async def get_event_details(contentid):
    result = get_event_info_by_id(contentid)  # ID로 이벤트 데이터 조회
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result