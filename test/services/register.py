from fastapi import HTTPException, status
from ..db import register_db
from ..models.register import (
    UserSchema,
    ManagerSchema,
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# 유저 id 중복 검사
def check_user_id_service(user_id: str):
    conn = register_db()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT id
            FROM user_info
            WHERE id = %s;
            """
            cursor.execute(sql, (user_id,))
            result = bool(cursor.fetchone())
            return not result  # True를 반환하도록 수정
    except Exception as e:
        print(f"ID 중복 확인 오류: {e}")
        raise HTTPException(status_code=500, detail="ID 중복 확인 오류")
    finally:
        conn.close()

# 기업회원 id 중복 조회
def check_manager_id_service(manager_id: str):
    conn = register_db()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT id
            FROM manager_info
            WHERE id = %s;
            """
            cursor.execute(sql, (manager_id,))
            result = bool(cursor.fetchone())
            return not result  # True를 반환하도록 수정
    except Exception as e:
        print(f"ID 중복 확인 오류: {e}")
        raise HTTPException(status_code=500, detail="ID 중복 확인 오류")
    finally:
        conn.close()

# 기업회원 phone 중복 조회
def check_manager_phone_service(manager_phone: str):
    conn = register_db()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT phone
            FROM manager_info
            WHERE phone = %s;
            """
            cursor.execute(sql, (manager_phone,))
            result = bool(cursor.fetchone())
            return not result  # True를 반환하도록 수정
    except Exception as e:
        print(f"전화번호 중복 확인 오류: {e}")
        raise HTTPException(status_code=500, detail="전화번호 중복 확인 오류")
    finally:
        conn.close()

# 유저 정보 삽입
def user_register_service(user: UserSchema):
    conn = register_db()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO user_info (name, nickname, id, password) VALUES (%s, %s, %s, %s)
            """
            result = cursor.execute(sql, (user.name, user.nickname, user.id, get_password_hash(user.password.get_secret_value()))) # 암호화된 비밀번호 저장
            conn.commit()
            return result
    except Exception as e:
        print(f"사용자 등록 오류: {e}")
        raise HTTPException(status_code=500, detail="사용자 등록 오류")
    finally:
        conn.close()

# 기업회원 정보 삽입
def manager_register_service(manager: ManagerSchema):
    conn = register_db()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO manager_info (company, name, phone, id, password) VALUES (%s, %s, %s, %s, %s)
            """
            result = cursor.execute(sql, (manager.company, manager.name, manager.phone.get_secret_value(), manager.id, get_password_hash(manager.password.get_secret_value()))) # 암호화된 비밀번호 저장
            conn.commit()
            return result
    except Exception as e:
        print(f"기업회원 등록 오류: {e}")
        raise HTTPException(status_code=500, detail="기업회원 등록 오류")
    finally:
        conn.close()