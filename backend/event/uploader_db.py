import os
import pymysql

def uploader_db():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER_X"),
            password=os.getenv("DB_USER_XPW"),
            db=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT")),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        return conn
    except Exception as e:
        print(f"데이터베이스 연결 오류: {e}")
        return None
    