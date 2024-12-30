from fastapi import HTTPException, status
import traceback
import os
import jwt_module

from db import login_db
from jwt_module.jwt_handler import (
    create_jwt_token,
    decode_jwt_token,
    refresh_jwt_token,
)

from login.model import (
    PersonalLogin,
    EnterpriseLogin,
    NaverLogin,
    KakaoLogin,
)

async def login_personal_service(personal_login: PersonalLogin):
    """
        일반회원 id, pw 기반 로그인 시도시 작동하는 서비스
    """
    secret_key = os.getenv("JWT_LOGIN_ACCESS_KEY")
    password_decrypt_key = os.getenv("DB_STR_KEY")
    conn = login_db()
    if not conn:
        # 데이터베이스 연결 오류
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")

    try:
        with conn.cursor() as cursor:
            # 1. 사용자 인증 (아이디, 비밀번호 확인) - 실제 인증 로직 구현
            sql = "SELECT user_id FROM user_info WHERE user_id = %s AND CAST(AES_DECRYPT(unhex(user_pw), SHA2(%s, 256)) AS CHAR(255)) = %s"
            cursor.execute(sql, (personal_login.user_id, password_decrypt_key, personal_login.user_pw,))  # user_pw 값을 추가
            user = cursor.fetchone()

            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Incorrect username or password, {user['user_pw']} is not {str(personal_login.user_pw)}",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # 2. JWT 토큰 생성
            access_token = create_jwt_token(user['user_id'], 1, secret_key)  # JWT secret key 설정

            return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="로그인 처리 오류")

    finally:
        conn.close()

async def login_enterprise_service(enterprise_login: EnterpriseLogin):
    """
        기업회원 id, pw 기반 로그인 시도시 작동하는 서비스
    """
    print(enterprise_login)
    secret_key = os.getenv("JWT_LOGIN_ACCESS_KEY")
    password_decrypt_key = os.getenv("DB_STR_KEY")
    conn = login_db()
    if not conn:
        # 데이터베이스 연결 오류
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")

    try:
        with conn.cursor() as cursor:
            # 1. 사용자 인증 (아이디, 비밀번호 확인) - 실제 인증 로직 구현
            sql = "SELECT manager_id FROM manager_info WHERE manager_id = %s AND CAST(AES_DECRYPT(unhex(manager_pw), SHA2(%s, 256)) AS CHAR(255)) = %s"
            cursor.execute(sql, (enterprise_login.manager_id, password_decrypt_key, enterprise_login.manager_pw))
            user = cursor.fetchone()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # 2. JWT 토큰 생성
            access_token = create_jwt_token(user['manager_id'], 2, secret_key)  # JWT secret key 설정

            return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="로그인 처리 오류")

    finally:
        conn.close()

async def login_naver_service(naver_login: NaverLogin):
    """
        네이버 간편로그인 시도시 작동하는 서비스
        네이버 로그인 성공시 해당 id만 들어오고 해당 id가 없다면 회원가입창으로 보내야함.
        아니면 회원가입 먼저 하고 연동시키는 방향으로?
    """
    secret_key = os.getenv("JWT_LOGIN_ACCESS_KEY")
    conn = login_db()
    if not conn:
        # 데이터베이스 연결 오류
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    
    try:
        with conn.cursor() as cursor:
            # 1. 사용자 인증 (아이디 확인)
            sql = "SELECT uid FROM user_info WHERE naver_id = %s"
            cursor.execute(sql, (naver_login.naver_id,))
            user = cursor.fetchone()

            if not user:
                # 2-1. naver_id가 없다면 회원가입 창으로 리디렉션 (프론트엔드에서 처리)
                return {"message": "naver_id not found", "redirect": True} 

            # 2-2. JWT 토큰 생성
            access_token = create_jwt_token(user['user_id'], 1, secret_key)
            return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="로그인 처리 오류")

    finally:
        conn.close()

async def login_kakao_service(kakao_login: KakaoLogin):
    """
        카카오 간편로그인 시도시 작동하는 서비스
        네이버 로그인 성공시 해당 id만 들어오고 해당 id가 없다면 회원가입창으로 보내야함.
        아니면 회원가입 먼저 하고 연동시키는 방향으로?
    """
    secret_key = os.getenv("JWT_LOGIN_ACCESS_KEY")
    conn = login_db()
    if not conn:
        # 데이터베이스 연결 오류
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")
    
    try:
        with conn.cursor() as cursor:
            # 1. 사용자 인증 (아이디 확인)
            sql = "SELECT uid FROM user_info WHERE naver_id = %s"
            cursor.execute(sql, (kakao_login.kakao_id,))
            user = cursor.fetchone()

            if not user:
                # 2-1. naver_id가 없다면 회원가입 창으로 리디렉션 (프론트엔드에서 처리)
                return {"message": "kakao_id not found", "redirect": True} 

            # 2-2. JWT 토큰 생성
            access_token = create_jwt_token(user['user_id'], 1, secret_key)
            return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print(f"로그인 처리 오류: {e}")
        raise HTTPException(status_code=500, detail="로그인 처리 오류")

    finally:
        conn.close()

async def check_user_service(token: str):
    """
        토큰을 기반으로 유저 정보를 확인하는 API
        Args:
            Token(str) : JWT 로그인 정보 토큰큰
        
        Return:
            Integer Code
            0 : Not User
            1 : Personal User
            2 : Company User
            3 : Simple Login User (Naver)
            4 : Simple Login User (Kakao)
            5 : Invaild Token
            6 : Expired Token
    """

    secret_key = os.getenv("JWT_LOGIN_ACCESS_KEY")
    conn = login_db()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    try:
        payload = decode_jwt_token(token, secret_key)
        if payload is None:
            return 5 # Invaild Token
        
        user_id = payload.get('user_id')
        user_type = payload.get('user_type')
        if user_id is None or user_type is None:
            return 0 # Not User
        
        return user_type
    
    except jwt_module.ExpiredSignatureError:
        return 6 # Expired Token
    except Exception as e:
        print(f"Functional Error: {e}")
        raise HTTPException(status_code=500, detail="Functional Error")
    finally:
        conn.close()

async def update_token_service(token: str):
    """
        토큰을 갱신시켜 리턴하는 API
        Args:
            token (str): jwt_token 
        Returns:
            str: new_jwt_token
    """
    secret_key = os.getenv("JWT_LOGIN_ACCESS_KEY")
    algorithm = "HS256"
    expire_minutes = 60
    try:
        new_token = refresh_jwt_token(token, secret_key, algorithm, expire_minutes)
        return new_token
    except jwt_module.ExpiredSigntureError:
        return None
    except jwt_module.InvaildTokenError:
        return None

async def decode_user_information_service(token: str):
    """
        인증된 토큰을 이용해 사용자 정보를 리턴하는 API
        Args:
            token (str): jwt_token
        Returns:
            dict: 디코딩된 페이로드
    """
    secret_key = os.getenv("JWT_LOGIN_ACCESS_KEY")
    algorithm = "HS256"
    payload = decode_jwt_token(token, secret_key, algorithm)
    return payload
