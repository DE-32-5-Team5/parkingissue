import jwt
from fastapi.responses import JSONResponse
from fastapi import Response
from datetime import datetime, timedelta

def create_jwt_token(user_id: int, user_type: int, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 60, response=None):
    """
    JWT 토큰 생성하는 함수

    Args:
        user_id (int): 사용자 ID
        user_type (int): 사용자 유형 코드 (1: 일반 사용자, 2: 기업 사용자)
        secret_key (str): JWT Secret Key
        algorithm (str, optional): JWT 알고리즘.
        expire_minutes (int, optional): 토큰 만료 시간 (분).
        response: FastAPI의 Response 객체, JWT 토큰을 쿠키에 설정하기 위해 사용

    Returns:
        str: JWT 토큰
    """

    if response is None:
        raise ValueError("response must be provided")

    # Payload 설정
    payload = {
        "user_id": user_id,
        "user_type": user_type,  # user_type 추가
        "exp": datetime.now() + timedelta(minutes=expire_minutes)
    }

    # JWT 토큰 생성
    token = jwt.encode(payload, secret_key, algorithm=algorithm)

    # 쿠키에 토큰 설정
    response.set_cookie(
        key="jwt_token",
        value=token,
        httponly=True,  # JavaScript에서 접근 불가
        secure=False,    # HTTPS에서만 전송
        samesite="Lax",  # CSRF 보호
        path="/",
        domain="parkingissue.online"
    )

    return {"message": "Login successful"}

def refresh_jwt_token(token: str, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 60):
    """
    JWT 토큰을 갱신하는 함수

    Args:
        token (str): 갱신할 JWT 토큰
        secret_key (str): JWT Secret Key
        algorithm (str, optional): JWT 알고리즘.
        expire_minutes (int, optional): 토큰 만료 시간 (분).

    Returns:
        str: 갱신된 JWT 토큰
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        # 만료 시간을 갱신합니다.
        payload['exp'] = datetime.now() + timedelta(minutes=expire_minutes)
        new_token = jwt.encode(payload, secret_key, algorithm=algorithm)
        return new_token
    except jwt.ExpiredSignatureError:
        # 토큰이 만료된 경우에는 None을 반환합니다.
        return None
    except jwt.InvalidTokenError:
        # 유효하지 않은 토큰인 경우에도 None을 반환합니다.
        return None

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
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        # 토큰이 만료된 경우에는 None을 반환합니다.
        return None
    except jwt.InvalidTokenError:
        # 유효하지 않은 토큰인 경우에도 None을 반환합니다.
        return None