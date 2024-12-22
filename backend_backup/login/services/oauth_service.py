from fastapi import HTTPException, status
from login.user.common_user import verify_password
from login.models.user_info import UserInfo
import aiomysql
from db import get_db

async def get_user_by_id(id: str):
    conn = await get_db()
    if conn:
        try:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM user_info WHERE user_id = %s", (id,))
                user_data = await cur.fetchone()
                if user_data:
                    return UserInfo(**user_data)
                return None
        except aiomysql.Error as e:
            print(f"Query execution error: {e}")
            return None
        finally:
            conn.close()
    return None


async def authenticate_user(id: str, password: str):
    user = await get_user_by_id(id=id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user.pw):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user