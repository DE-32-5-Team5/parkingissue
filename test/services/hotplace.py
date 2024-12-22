from fastapi import HTTPException, status
from ..db import hotplace_db  # db 연결 함수 import
from ..models.location import Location  # Location 모델 import

async def hotplace_default_list_service(location: Location):
    conn = hotplace_db()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT contentid, title, eventstartdate, eventenddate, firstimage, mapx, mapy,
                (6371 * acos(cos(radians(%s)) * cos(radians(mapy)) * 
                cos(radians(mapx) - radians(%s)) + sin(radians(%s)) * sin(radians(mapy)))) AS distance
            FROM festival_info
            WHERE eventstartdate <= NOW() AND eventenddate >= NOW()
            ORDER BY distance ASC
            """
            cursor.execute(sql, (location.latitude, location.longitude, location.latitude))  # Location 객체 사용
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"핫플레이스 기본 리스트 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="핫플레이스 기본 리스트 조회 오류")
    finally:
        conn.close()

async def hotplace_ongoing_list_service():
    conn = hotplace_db()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT contentid, title, eventstartdate, eventenddate, firstimage, mapx, mapy
            FROM festival_info
            WHERE eventstartdate >= NOW() AND eventenddate >= NOW()
            ORDER BY eventstartdate ASC
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"핫플레이스 진행중 리스트 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="핫플레이스 진행중 리스트 조회 오류")
    finally:
        conn.close()

async def hotplace_upcoming_list_service():
    conn = hotplace_db()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT contentid, title, eventstartdate, eventenddate, firstimage, mapx, mapy
            FROM festival_info
            WHERE eventstartdate >= NOW() AND eventenddate >= NOW()
            ORDER BY eventstartdate ASC
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"핫플레이스 예정 리스트 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="핫플레이스 예정 리스트 조회 오류")
    finally:
        conn.close()

# async def hotplace_adress_list_service(resion: str):
#     conn = hotplace_db()
#     if not conn:
#         raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
#     try:
#         with conn.cursor() as cursor:
#             sql = """
#             SELECT contentid, title, eventstartdate, eventenddate, firstimage, mapx, mapy
#             FROM festival_info
#             WHERE address LIKE %s
#             """
#             cursor.execute(sql, (f"%{resion}%",))  # LIKE 검색을 위한 % 추가
#             result = cursor.fetchall()
#             return result
#     except Exception as e:
#         print(f"핫플레이스 지역 리스트 조회 오류: {e}")
#         raise HTTPException(status_code=500, detail="핫플레이스 지역 리스트 조회 오류")
#     finally:
#         conn.close()

async def hotplace_content_info_service(contentid: str):
    conn = hotplace_db()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT *
            FROM festival_info
            WHERE contentid = %s;
            """
            cursor.execute(sql, (contentid,))
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"핫플레이스 상세 정보 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="핫플레이스 상세 정보 조회 오류")
    finally:
        conn.close()