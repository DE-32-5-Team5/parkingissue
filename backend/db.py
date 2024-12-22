import os
import pymysql

"""
    Parkingissue Database 연결 함수 모음집
    각 기능에 해당하는 쪽으로 함수를 가져가세요.

    로그인 : login_db()
    회원가입 : register_db()
    메인페이지, 검색 : location_db()
    스파크, 카프카 : spark_db()
    에어플로우 : airflow_db()
    게시글 업로드 : uploader_db()
"""

def login_db():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_LOGIN_USER"),
            password=os.getenv("DB_LOGIN_PASSWORD"),
            db=os.getenv("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        return conn
    except Exception as e:
        print(f"데이터베이스 연결 오류: {e}")
        return None

def register_db():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_REGISTER_USER"),
            password=os.getenv("DB_REGISTER_PASSWORD"),
            db=os.getenv("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        return conn
    except Exception as e:
        print(f"데이터베이스 연결 오류: {e}")
        return None

def location_db():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_LOCATION_USER"),
            password=os.getenv("DB_LOCATION_PASSWORD"),
            db=os.getenv("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        return conn
    except Exception as e:
        print(f"데이터베이스 연결 오류: {e}")
        return None
    
def spark_db():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_SPARK_USER"),
            password=os.getenv("DB_SPARK_PASSWORD"),
            db=os.getenv("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        return conn
    except Exception as e:
        print(f"데이터베이스 연결 오류: {e}")
        return None
    
def airflow_db():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_AIRFLOW_USER"),
            password=os.getenv("DB_AIRFLOW_PASSWORD"),
            db=os.getenv("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        return conn
    except Exception as e:
        print(f"데이터베이스 연결 오류: {e}")
        return None
    
def uploader_db():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_UPLOADER_USER"),
            password=os.getenv("DB_UPLOADER_PASSWORD"),
            db=os.getenv("DB_NAME"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        return conn
    except Exception as e:
        print(f"데이터베이스 연결 오류: {e}")
        return None