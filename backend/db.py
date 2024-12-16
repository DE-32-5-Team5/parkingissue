import aiomysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_LOGIN_ID")
DB_PASSWORD = os.getenv("DB_LOGIN_PW")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

async def get_db():
    try:
        conn = await aiomysql.connect(
            host=DB_HOST,
            port=int(DB_PORT), #port는 int형이어야 함
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            autocommit=True, # autocommit 설정
            cursorclass=aiomysql.DictCursor # 결과를 딕셔너리로 받기 위함
        )
        return conn
    except aiomysql.Error as e:
        print(f"Database connection error: {e}")
        return None

async def get_user_by_id(id: str):
    conn = await get_db()
    if conn:
        try:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM user_info WHERE id = %s", (email,))
                user = await cur.fetchone()
                return user
        except aiomysql.Error as e:
            print(f"Query execution error: {e}")
            return None
        finally: # connection close 추가
            conn.close()
    return None

async def get_all_users():
    conn = await get_db()
    if conn:
        try:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM user_info")
                users = await cur.fetchall()
                return users
        except aiomysql.Error as e:
            print(f"Query execution error: {e}")
            return None
        finally: # connection close 추가
            conn.close()
    return None