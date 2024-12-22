from pydantic import BaseModel, SecretStr 

class UserInfo(BaseModel):
    """
        user_info
        uid
        user_id
        user_pw
        user_name
        user_nickname
        naver_id
        kakao_id
    """
    user_id: str
    user_pw: SecretStr
    user_name: str
    user_nickname: str
    naver_id: str
    kakao_id: str