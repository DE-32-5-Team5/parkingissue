import jwt
from datetime import datetime, timedelta

def create_jwt_token(user_id:int, secret_key:str, algorithm: str = "HS256", expire_minutes: int = 60):
    """
        JWT 토큰 생성하는 함수

        Args:
            user_id (int): 사용자 ID
            secret_key (str): JWT Secret Key
            algorithm (str, optional): JWT 알고리즘.
            expire_minutes (int, optional): 토큰 만료 시간 (분).
        
        Returns:
            str: JWT 토큰
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=expire_minutes)
    }
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token
    