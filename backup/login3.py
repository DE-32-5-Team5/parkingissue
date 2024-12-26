from pydantic import BaseModel, SecretStr 

class PersonalLogin(BaseModel):
    user_id: str
    user_pw: str

class EnterpriseLogin(BaseModel):
    manager_id: str
    manager_pw: str

class NaverLogin(BaseModel):
    naver_id: str

class KakaoLogin(BaseModel):
    kakao_id: str