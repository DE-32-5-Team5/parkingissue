from fastapi import HTTPException, status, Request, Response
import traceback
import os
from jwtM.jwt_handler import decode_jwt_token
import jwt
from db import login_db

async def check_user_service(request: Request):
    """
        토큰을 기반으로 유저 정보를 확인하는 API
        Args:
            Token(str) : JWT 로그인 정보 토큰

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
    token = request.cookies.get("jwt_token")

    secret_key = os.getenv("JWT_LOGIN_ACCESS_KEY")
    conn = login_db()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection error")
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    try:
        payload = decode_jwt_token(token, secret_key)
        if payload is None:
            return 5 # Invaild Token

        user_id = payload.get('user_id')
        user_type = payload.get('user_type')
        if user_id is None or user_type is None:
            return 0 # Not User

        return user_type, user_id

    except jwt.ExpiredSignatureError:
        return 6 # Expired Token
    except Exception as e:
        print(f"Functional Error: {e}")
        raise HTTPException(status_code=500, detail="Functional Error")
    finally:
        conn.close()

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

