from login.models.user_info import UserInfo, UserInfoCreate
from login.user.common_user import hash_password, verify_password
from db import get_user_by_id, get_all_users, create_user, get_db


async def create_user(user: UserInfoCreate):
    conn = await get_db()
    if conn:
        try:
            async with conn.cursor() as cur:
                hashed_password = hash_password(user.pw)
                await cur.execute(
                    "INSERT INTO user_info (user_id, pw, name) VALUES (%s, %s, %s)",
                    (user.id, hashed_password, user.name),
                )
                return await get_user_by_id(user.id)
        except aiomysql.Error as e:
            print(f"Query execution error: {e}")
            return None
        finally:
            conn.close()
    return None


async def get_user_by_id(id: str):
    user_data = await get_user_by_id(id=id)
    if user_data:
        return UserInfo(**user_data)  # dict를 pydantic 모델로 변환
    return None


async def get_all_users():
    users_data = await get_all_users()
    user_list = []
    if users_data:
        for user_data in users_data:
            user = UserInfo(**user_data)
            user_list.append(user)
    return user_list