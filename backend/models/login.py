from pydantic import BaseModel, SecretStr 

class PersonalLogin(BaseModel):
    user_id: str
    user_pw: SecretStr

class EnterpriseLogin(BaseModel):
    manager_id: str
    manager_pw: SecretStr

class NaverLogin(BaseModel):
    naver_id: str

class KakaoLogin(BaseModel):
    kakao_id: str