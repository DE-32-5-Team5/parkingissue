from fastapi import FastAPI, Form, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from .database import get_db
from .models import FestivalInfo
import os, uuid, logging
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI(docs_url='/api2/docs', openapi_url='/api2/openapi.json')

# CORS 설정 활성화 - 프론트랑 백엔드 포트가 달라서 브라우저가 막아놓음
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

UPLOAD_DIR = "uploads/"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 이벤트 등록 엔드포인트
@app.post("/event-registration/")
async def register_event(
    title: str = Form(...),
    address: str = Form(...),
    contact: str = Form(...), 
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),  
    main_image: UploadFile = File(...),  
    thumbnail_image: UploadFile = File(...),  
    mapx: float = Form(...),  
    mapy: float = Form(...),  
    description: str = Form(...),
    db: Session = Depends(get_db)  
):
    main_image_filename = f"{uuid.uuid4().hex}_{main_image.filename}"
    thumbnail_image_filename = f"{uuid.uuid4().hex}_{thumbnail_image.filename}"
    
    # 파일 경로 설정정
    main_image_path = os.path.join(UPLOAD_DIR, main_image_filename)
    thumbnail_image_path = os.path.join(UPLOAD_DIR, thumbnail_image_filename)

    # 이미지 파일 저장
    try:
        with open(main_image_path, "wb") as f:
            f.write(await main_image.read())
        
        with open(thumbnail_image_path, "wb") as f:
            f.write(await thumbnail_image.read())
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="이미지 저장에 실패했습니다.")
    
    # # 전화번호 저장 (전화번호를 '-'로 구분하여 하나의 문자열로 저장)
    tel = contact

    # FestivalInfo 객체 생성 (폼 데이터와 함께)
    event = FestivalInfo(
        title=title,
        address=address,
        eventstartdate=datetime.strptime(start_date, "%Y-%m-%d").date(),
        eventenddate=datetime.strptime(end_date, "%Y-%m-%d").date(),
        tel=tel,
        firstimage=main_image_path,  # 파일 경로 저장
        firstimage2=thumbnail_image_path,  # 파일 경로 저장
        mapx=mapx,
        mapy=mapy,
        description=description
    )

    # 데이터베이스에 이벤트 저장
    try:
        db.add(event)
        db.commit()
        db.refresh(event)
    except Exception as e:
        db.rollback()  # 오류 발생 시 롤백
        logging.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="이벤트 등록에 실패했습니다.")
    
    
    return {"message": "행사 등록 완료", "fid": event.fid}



