from fastapi import HTTPException
import os, uuid
from datetime import datetime
from db import uploader_db
from models.event import FestivalInfo

async def register_event_service(festival_info: FestivalInfo):

    conn = uploader_db()
    if not conn:
        raise HTTPException(status_code = 500, detail = "Database Connection Error")
    
    UPLOAD_DIR = "uploads/"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    if festival_info.firstimage:
        main_image_filename = f"{uuid.uuid4().hex}_{festival_info.firstimage.filename}"
        main_image_path = os.path.join(UPLOAD_DIR, main_image_filename)
        with open(main_image_path, "wb") as f:
            f.write(await festival_info.firstimage.read())

    if festival_info.firstimage2:
        sub_image_filename = f"{uuid.uuid4().hex}_{festival_info.firstimage2.filename}"
        sub_image_path = os.path.join(UPLOAD_DIR, sub_image_filename)
        with open(sub_image_path, "wb") as f:
            f.write(await festival_info.firstimage2.read())

    event = FestivalInfo(
        title = festival_info.title,
        address = festival_info.address,
        eventstartdate = datetime.strptime(festival_info.eventstartdate, "%T-%m-%d").date(),
        eventenddate = datetime.strptime(festival_info.eventenddate, "%T-%m-%d").date(),
        tel = festival_info.tel,
        firstimage = main_image_path,
        firstimage2 = sub_image_path,
        mapx = festival_info.mapx,
        mapy = festival_info.mapy,
        description = festival_info.description
    )

    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 실행
            sql = """
                INSERT INTO festival_info (
                    title, address, eventstartdate, eventenddate, tel, 
                    firstimage, firstimage2, mapx, mapy, description
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                festival_info.title, 
                festival_info.address, 
                festival_info.eventstartdate, 
                festival_info.eventenddate, 
                festival_info.tel, 
                main_image_path,  # 이미지 경로 사용
                sub_image_path,  # 이미지 경로 사용
                festival_info.mapx, 
                festival_info.mapy, 
                festival_info.description
            ))
        conn.commit()  # 변경 사항 커밋

    except Exception as e:
        conn.rollback()  # 오류 발생 시 롤백
        print(f"이벤트 등록 오류: {e}")
        raise HTTPException(status_code=500, detail="이벤트 등록 오류")

    finally:
        conn.close()

    return {"message": "이벤트가 성공적으로 등록되었습니다."}