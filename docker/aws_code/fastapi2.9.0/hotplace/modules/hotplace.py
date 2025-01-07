import pymysql.cursors

def connect_db():
    connection = pymysql.connect(
        host='10.0.4.80',
        port=6033,
        user='root',
        password='samdul2024$',
        database='parkingissue',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection 
# festival_info 테이블 가까운순 목록 조회
def select_hotplace_default_info(hotplace_longitude, hotplace_latitude):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT contentid, title, eventstartdate, eventenddate, firstimage, mapx, mapy,
                   (6371 * acos(cos(radians(%s)) * cos(radians(mapy)) * 
                   cos(radians(mapx) - radians(%s)) + sin(radians(%s)) * sin(radians(mapy)))) AS distance
            FROM festival_info
            WHERE eventstartdate <= NOW() AND eventenddate >= NOW()
            ORDER BY distance ASC
            """
            cursor.execute(sql, (hotplace_latitude, hotplace_longitude, hotplace_latitude))
            result = cursor.fetchall()
            return result

# festival_info 테이블 진행중 목록 조회        
def select_hotplace_ongoing_info():
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT contentid, title, eventstartdate, eventenddate, firstimage, mapx, mapy
            FROM festival_info
            WHERE eventstartdate <= NOW() AND eventenddate >= NOW()
            ORDER BY eventstartdate ASC
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

# festival_info 테이블 아직 시작안한 목록 조회        
def select_hotplace_upcoming_info():
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT contentid, title, eventstartdate, eventenddate, firstimage, mapx, mapy
            FROM festival_info
            WHERE eventstartdate >= NOW() AND eventenddate >= NOW()
            ORDER BY eventstartdate ASC
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

# festival_info 테이블 지역 목록 조회        
# def select_hotplace_address_info(resion):
#     connection = connect_db()

#     with connection:
#         with connection.cursor() as cursor:
#             sql = """
#             SELECT contentid, title, eventstartdate, eventenddate, firstimage, mapx, mapy,
#             FROM festival_info
#             WHERE address like '%s%'
#             """
#             cursor.execute(sql)
#             result = cursor.fetchone()
#             return result

# festival_info 게시글 내용 조회
def select_hotplace_content(contentid):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT *
            FROM festival_info
            WHERE contentid = %s;
            """
            cursor.execute(sql, (contentid,))
            result = cursor.fetchone()
            return result
