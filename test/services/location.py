from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..db import location_db
from ..services.kafka_producer import send_to_kafka, send_to_kafka2
from ..models.location import Location, FromSpark

stored_data = []

async def create_item_service(location: Location):
    """
    위도, 경도 정보를 받아 Kafka에 전송하는 서비스
    """
    try:
        print(location)
        send_to_kafka({"latitude": str(location.latitude), "longitude": str(location.longitude)})
        return {"latitude": str(location.latitude), "longitude": str(location.longitude)}
    except Exception as e:
        print(f"Kafka 메시지 전송 오류: {e}")
        raise HTTPException(status_code=500, detail="Kafka 메시지 전송 오류")

async def receive_location_service(sparkdata: list[FromSpark]):
    """
    Spark에서 처리된 주차장 정보를 받아 저장하는 서비스
    """
    global stored_data
    stored_data = []
    stored_data.extend(sparkdata)
    return {"message": "Data received and stored successfully.", "stored_data": stored_data}

async def frontget_service():
    """
    저장된 주차장 정보를 프론트엔드에 제공하는 서비스
    """
    if not stored_data:
        return {"message": "데이터가 없습니다."}
    encoded_data = jsonable_encoder(stored_data)
    response = JSONResponse(content={"stored_data": encoded_data})
    response.headers["Cache-Control"] = "no-store"
    return response

async def get_park_info_service(parkid: str):
    """
    주차장 ID를 받아 주차장 정보를 반환하는 서비스
    """
    conn = location_db()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT
                i.park_id AS park_id,
                f.free_time AS free_time,
                f.basic_time AS basic_time,
                f.basic_charge AS basic_charge,
                f.additional_time AS additional_time,
                f.additional_charge AS additional_charge,
                f.daily_charge AS daily_charge,
                f.monthly_charge AS monthly_charge,
                o.wee_orn_st AS wee_orn_st,
                o.wee_orn_et AS wee_orn_et,
                o.wk_orn_st AS wk_orn_st,
                o.wk_orn_et AS wk_orn_et,
                o.hol_orn_st AS hol_orn_st,
                o.hol_orn_et AS hol_orn_et,
                TIME_TO_SEC(TIMEDIFF(o.wee_orn_et, o.wee_orn_st)) AS weekly,
                TIME_TO_SEC(TIMEDIFF(o.wk_orn_et, o.wk_orn_st)) AS weekend,
                TIME_TO_SEC(TIMEDIFF(o.hol_orn_et, o.hol_orn_st)) AS holiday
            FROM
                parkingarea_info AS i
            LEFT JOIN
                parkingarea_fee AS f ON i.park_id = f.park_id
            LEFT JOIN
                parkingarea_opertime AS o ON i.park_id = o.park_id
            WHERE
                i.park_id = %s;
            """
            cursor.execute(sql, (parkid,))
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"주차장 정보 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="주차장 정보 조회 오류")
    finally:
        conn.close()

async def get_related_data_service(text: str):
    """
    주차장 이름을 기반으로 유사한 주차장 정보를 반환하는 서비스
    """
    conn = location_db()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    try:
        with conn.cursor() as cursor:
            sql = f"""
            SELECT park_nm AS {text}
            FROM parkingarea_info
            WHERE park_nm LIKE '%{text}%'
            LIMIT 5;
            """
            cursor.execute(sql,)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"유사 주차장 정보 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="유사 주차장 정보 조회 오류")
    finally:
        conn.close()

async def get_click_search_service(txt: str):
    """
    검색어를 Kafka에 전송하는 서비스
    """
    try:
        send_to_kafka2({'search_msg': txt})
        print('연관 검색어 카프카 전송 완료')
        return {'search_msg': txt}
    except Exception as e:
        print(f"Kafka 메시지 전송 오류: {e}")
        raise HTTPException(status_code=500, detail="Kafka 메시지 전송 오류")