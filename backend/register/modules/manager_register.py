import pymysql.cursors
from db import register_db


# 기업회원 id 중복 조회
def check_manager_id(manager_id):
    connection = register_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT id
            FROM manager_info
            WHERE manager_id = %s;
            """
            cursor.execute(sql, (manager_id,))
            result = bool(cursor.fetchone())
            return result
        
# 기업회원 phone 중복 조회
def check_manager_phone(manager_id):
    connection = register_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT phone
            FROM manager_info
            WHERE manager_id = %s;
            """
            cursor.execute(sql, (manager_id,))
            result = bool(cursor.fetchone())
            return result
        
# 기업회원 정보 삽입
def insert_manager_info(manager_company, manager_name, manager_phone, manager_id, manager_password):
    connection = register_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO manager_info (company, name, phone, manager_id, manager_pw) VALUES (%s, %s, %s, %s, %s)
            """
            result = bool(cursor.execute(sql, (manager_company, manager_name, manager_phone, manager_id, manager_password)))
            
            return result
