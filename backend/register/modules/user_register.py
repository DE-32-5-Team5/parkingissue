import pymysql.cursors
from db import register_db
import os
 
# 유저 id 중복 검사
def check_user_id(user_id):
    connection = register_db()
        
    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT user_id
            FROM user_info
            WHERE user_id = %s;
            """
            cursor.execute(sql, (user_id,))
            result = bool(cursor.fetchone())
            return result
        
# 유저 정보 삽입
def insert_user_info(user_name, user_nick, user_id, user_pw):
    connection = register_db()
    crypt_key = os.getenv("DB_STR_KEY")
    with connection:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO user_info (user_name, user_nick, user_id, user_pw) VALUES (%s, %s, %s, HEX(AES_ENCRYPT(%s, SHA2(%s, 256))))
                """
            cursor.execute(sql, (user_name, user_nick, user_id, user_pw, crypt_key))
            connection.commit()  # 커밋을 명시적으로 수행
            print("데이터 삽입 성공")
            return True
