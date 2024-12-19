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
# festival_info 테이블 목록 조회
def select_hotplace_list_info(hotplace_longitude, hotplace_laitude):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT title, eventstartdate, eventenddate, mapx, mapy
            FROM festival_info
            WHERE
            """
            cursor.execute(sql, (,))
            result = bool(cursor.fetchone())
            return result
# festival_info 게시글 내용 조회
def check_manager_phone(manager_phone):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT phone
            FROM manager_info
            WHERE id = %s;
            """
            cursor.execute(sql, (user_id,))
            result = bool(cursor.fetchone())
            return result
# 기업회원 정보 삽입
def insert_manager_info(manager_company, manager_name, manager_phone, manager_id, manager_password):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO manager_info (company, name, phone, id, password) VALUES (%s, %s, %s, %s, %s)
            """
            result = bool(cursor.execute(sql, (manager_company, manager_name, manager_phone, manager_id, manager_password)))
            
            return result