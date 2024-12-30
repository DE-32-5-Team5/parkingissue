import pymysql.cursors
from db import register_db
import os


# 기업회원 id 중복 조회
def check_manager_id(manager_id):
    connection = register_db()

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
    connection = register_db()

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
    connection = register_db()
    crypt_key = os.getenv("DB_STR_KEY")

    with connection:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO manager_info (manager_company, manager_name, manager_phone, manager_id, manager_password) VALUES (%s, %s, %s, %s, %s)
                """
            cursor.execute(sql, (manager_company, manager_name, manager_phone, manager_id, manager_password))
            connection.commit()  # 커밋을 명시적으로 수행
            print("데이터 삽입 성공")
            return True
