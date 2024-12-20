import pymysql.cursors
import mysql.connector

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
# 기업회원 id 중복 조회
def check_manager_id(manager_id):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT manager_id
            FROM manager_info
            WHERE manager_id = %s;
            """
            cursor.execute(sql, (manager_id,))
            result = bool(cursor.fetchone())
            return result
# 기업회원 phone 중복 조회
def check_manager_phone(manager_phone):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT manager_phone
            FROM manager_info
            WHERE manager_phone = %s;
            """
            cursor.execute(sql, (manager_phone,))
            result = bool(cursor.fetchone())
            return result
# 기업회원 정보 삽입
def insert_manager_info(manager_company, manager_name, manager_phone, manager_id, manager_password):
    connection = connect_db()
    try:
        with connection:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO manager_info (manager_company, manager_name, manager_phone, manager_id, manager_password) VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (manager_company, manager_name, manager_phone, manager_id, manager_password))
                connection.commit()  # 커밋을 명시적으로 수행
                print("데이터 삽입 성공")
                return True
    except Exception as e:
        # 에러 로그 출력
        print("데이터 삽입 중 에러 발생!")
        print(f"에러 메시지: {e}")
        print(f"SQL: {sql}")
        print(f"파라미터: {user_name}, {user_nick}, {user_id}, {user_pw}")
        return False