import pymysql.cursors
import random
import os
import requests
from db import uploader_db, login_db
from dotenv import load_dotenv

load_dotenv(override=True)

def get_xy(region):
    k_key = os.getenv('KAKAO_REST')
    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    headers = {'Authorization': f'KakaoAK {k_key}'}
    params = {'query' : region, 'analyze_type' : 'similar', 'size' : 30}

    res = requests.get(url, params = params, headers = headers).json()

    return res
def select_name(idtype,idcode):
    if idtype not in ["uid", "mid"]:
        raise ValueError("Invalid idtype. Must be 'uid' or 'mid'.")
    tableNm2 = "user_info" if idtype == "uid" else "manager_info"
    colNm = "user_id" if idtype == "uid" else "manager_id"
    colNm2 = "user_name" if idtype == "uid" else "manager_name"
    colNm3 = "user_nick" if idtype == "uid" else "manager_company"
    connection = login_db()
    #print("$"*100)
    #print(idtype)
    #print(idcode)
    with connection:
        with connection.cursor() as cursor:
            # SQL 쿼리 작성
            sql = f"""
            SELECT {colNm2}, {colNm3} FROM {tableNm2}
            WHERE
                {colNm} = '{idcode}'
            """
            print(sql)
            print("$"*100)
            # 쿼리 실행
            result = cursor.execute(sql)
            print(colNm3)
            print(result)
            name_row = cursor.fetchall()
            print(name_row)
            return name_row

def generate_unique_id(c_ID, cursor):
    """데이터베이스에서 중복되지 않는 ID 생성"""
    while True:
        random_id = random.randint(100000, 999999)  # 6자리 랜덤 숫자 생성
        cursor.execute("SELECT COUNT(*) AS count FROM festival_info WHERE contentid = %s", (f"{c_ID}_{random_id}",))
        result = cursor.fetchone()
        if result['count'] == 0:  # 중복되지 않는 ID 발견
            return f"{c_ID}_{random_id}"

def insert_event_info(c_ID, title, address, contact, start_date, end_date, main_image_path, thumbnail_image_path, description):
    connection = uploader_db()
    # 주소 위경도 변환
    result = get_xy(address)
    add_xy = result['documents']
    #print("****")
    #print(add_xy)
    #x = add_xy[0]['address']['x']
    #y = add_xy[0]['address']['y']
    x = add_xy[0]['x']
    y = add_xy[0]['y']

    print(c_ID, title, address, contact, x, y)
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
                    main_image_path, thumbnail_image_path, x, y, description
                ))
                connection.commit()  # 커밋을 명시적으로 수행
                print(f"데이터 삽입 성공: ID={c_ID}")
                return True
    except Exception as e:
        print(f"데이터 삽입 실패: {e}")
        return False

def get_event_info(id):
    connection = uploader_db()
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
    connection = uploader_db()
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