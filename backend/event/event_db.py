import pymysql.cursors
import random

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

def generate_unique_id(c_ID, cursor):
    """데이터베이스에서 중복되지 않는 ID 생성"""
    while True:
        random_id = random.randint(100000, 999999)  # 6자리 랜덤 숫자 생성
        cursor.execute("SELECT COUNT(*) AS count FROM festival_info WHERE contentid = %s", (f"{c_ID}_{random_id}",))
        result = cursor.fetchone()
        if result['count'] == 0:  # 중복되지 않는 ID 발견
            return f"{c_ID}_{random_id}"

def insert_event_info(c_ID, title, address, contact, start_date, end_date, main_image_path, thumbnail_image_path, description):
    connection = connect_db()
    print(c_ID, title, address, contact)
    try:
        with connection:
            with connection.cursor() as cursor:
                # 고유 ID 생성
                if '_' not in c_ID:
                    c_ID = generate_unique_id(c_ID, cursor)

                # SQL 쿼리
                sql = """
                    INSERT INTO festival_info
                    (contentid, title, address, eventstartdate, eventenddate, tel, firstimage, firstimage2, mapx, mapy, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    title = VALUES(title),
                    address = VALUES(address),
                    eventstartdate = VALUES(eventstartdate),
                    eventenddate = VALUES(eventenddate),
                    tel = VALUES(tel),
                    firstimage = VALUES(firstimage),
                    firstimage2 = VALUES(firstimage2),
                    mapx = VALUES(mapx),
                    mapy = VALUES(mapy),
                    description = VALUES(description)
                """
                cursor.execute(sql, (
                    c_ID, title, address, start_date, end_date, contact,
                    main_image_path, thumbnail_image_path, 0.0, 0.0, description
                ))
                connection.commit()  # 커밋을 명시적으로 수행
                print(f"데이터 삽입 성공: ID={c_ID}")
                return True
    except Exception as e:
        print(f"데이터 삽입 실패: {e}")
        return False

def get_event_info(id):
    connection = connect_db()
    try:
        with connection:
            with connection.cursor() as cursor:
                sql = """
                    SELECT *
                    FROM festival_info
                    WHERE contentid LIKE %s;
                """
                param = f"{id}%"
                cursor.execute(sql, (param,))
                results = cursor.fetchall()
                return results
    except Exception as e:
        # 에러 로그 출력
        print("데이터 조회 중 에러 발생!")
        print(f"에러 메시지: {e}")
        return False

def get_event_info_by_id(contentid):
    connection = connect_db()
    try:
        with connection:
            with connection.cursor() as cursor:
                sql = """
                    SELECT *
                    FROM festival_info
                    WHERE contentid = %s;
                """
                cursor.execute(sql, (contentid,))
                results = cursor.fetchall()
                return results
    except Exception as e:
        # 에러 로그 출력
        print("데이터 조회 중 에러 발생!")
        print(f"에러 메시지: {e}")
        return False
