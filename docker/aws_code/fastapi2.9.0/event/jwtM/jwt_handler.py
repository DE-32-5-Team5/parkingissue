import jwt as j
from fastapi.responses import JSONResponse
from fastapi import Response
from datetime import datetime, timedelta

def decode_jwt_token(token: str, secret_key: str, algorithm: str = "HS256"):
    """
    JWT 토큰을 디코딩하는 함수

    Args:
        token (str): 디코딩할 JWT 토큰
        secret_key (str): JWT Secret Key
        algorithm (str, optional): JWT 알고리즘.

    Returns:
        dict: 디코딩된 페이로드 또는 None
    """
    try:
        payload = j.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except j.ExpiredSignatureError:
        # 토큰이 만료된 경우에는 None을 반환합니다.
        return None
    except j.InvalidTokenError:
        # 유효하지 않은 토큰인 경우에도 None을 반환합니다.
        return None
