import pymysql.cursors
from db import register_db

 
# 유저 id 중복 검사
def check_user_id(user_id):
    connection = register_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT id
            FROM user_info
            WHERE user_id = %s;
            """
            cursor.execute(sql, (user_id,))
            result = bool(cursor.fetchone())
            return result
        
# 유저 정보 삽입
def insert_user_info(user_name, user_nick, user_id, user_pw):
    connection = register_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO user_info (name, nickname, user_id, user_pw) VALUES (%s, %s, %s, %s)
            """
            result = bool(cursor.execute(sql, (user_name, user_nick, user_id, user_pw)))
            return result
