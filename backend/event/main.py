from fastapi import FastAPI, Form, File, UploadFile, HTTPException, Query
import os
import json
import uuid
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi.responses import JSONResponse
from model import EventModel
from event_db import insert_event_info, get_event_info, get_event_info_by_id
from fastapi.staticfiles import StaticFiles
import boto3

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

def generate_unique_filename(filename: str) -> str:
    ext = filename.split(".")[-1]
    unique_name = f"{uuid.uuid4()}.{ext}"
    return unique_name

# S3 클라이언트 생성
s3_client = boto3.client('s3', region_name='ap-northeast-2')  # 리전 설정
bucket_name = 'fiveguys-s3'

def upload_and_get_url(file: UploadFile, file_key: str):
    try:
        # 파일을 S3에 직접 업로드
        s3_client.upload_fileobj(file.file, bucket_name, file_key, ExtraArgs={"ContentType": file.content_type})

        # 퍼블릭 URL 생성
        url = f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_key}"
        return url
    except Exception as e:
        print(f"Failed to upload {file_key}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload {file_key}: {e}")


# 이벤트 등록 엔드포인트
@app.post("/api2/event-registration")
async def register_event(
    event_data: str = Form(...),
    main_image: UploadFile = File(...),
    thumbnail_image: UploadFile = File(...),
):
    try:
        # event_data 파싱 및 유효성 검사
        parsed_event_data = json.loads(event_data)
        event = EventModel(**parsed_event_data)  # Pydantic 유효성 검사
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid event_data format: {str(e)}")

    # 고유한 파일 이름 생성
    main_image_filename = generate_unique_filename(main_image.filename)
    thumbnail_image_filename = generate_unique_filename(thumbnail_image.filename)

    # S3에 파일 업로드
    main_image_url = upload_and_get_url(main_image, f"images/{main_image_filename}")
    thumbnail_image_url = upload_and_get_url(thumbnail_image, f"images/{thumbnail_image_filename}")

    # 데이터베이스에 저장
    if insert_event_info(
        event.c_id, event.title, event.address, event.contact,
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
    if not results:
        return {"error": f"ID {ID}에 해당하는 이벤트가 없습니다."}

    return {"id": ID, "events": results}

# 이벤트 카드 클릭했을 때
from fastapi.responses import RedirectResponse
@app.get("/api2/event-details")
async def event_details(contentid: str):
    if not contentid:  # 특정 조건에 따라 리다이렉션
        return {"error": f"contentid 없음"}

    # 정상 처리 로직
    print(f"------ {contentid} ----")
    result = get_event_info_by_id(contentid)
    if not result:
        raise HTTPException(status_code=404, detail="등록한 행사 없음")
    return result


# 주소 자동완성
import requests
@app.get("/api2/search_address")
def search_address(query: str = Query(..., min_length=2)):
    kakao_key = os.getenv("KAKAO_REST")  # 환경 변수에서 API 키 로드
    if not kakao_key:
        return {"error": "Kakao API key not found"}

    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {kakao_key}"}
    params = {"query": query, "analyze_type": "similar", "size": 30}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # HTTP 상태 코드 확인
        data = response.json()
        if not data.get("documents"):
            print(f'--------------- { data.get("documents") } -----------')
            return {"error": "존재하지 않는 주소입니다."}
        return data
    except requests.exceptions.RequestException as e:
        return {"error": "Request failed", "details": str(e)}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}