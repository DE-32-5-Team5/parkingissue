from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta
import bcrypt
import requests  # 네이버/카카오 API 호출용
from db import get_user, get_manager, create_user  # DB 쿼리 함수 (가정)
from typing import Optional
from pydantic import BaseModel

class OAuthUserInfo(BaseModel):
    id: str
    email: Optional[str] = None
    nickname: Optional[str] = None

SECRET_KEY = "YOUR_SECRET_KEY"  # 환경변수 등으로 관리해야 함!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") #토큰 발급 url 임의지정

def generate_jwt(user_id, user_role):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user_id), "role": user_role, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))

async def login(user_id, password, login_type):
    if login_type == 1:
        user = await get_user(user_id)
    elif login_type == 2:
        user = await get_manager(user_id)
    else:
        raise HTTPException(status_code=400, detail="Invalid login type")

    if user and verify_password(password, user.password):
        token = generate_jwt(user.userid if login_type == 1 else user.managerid, "user" if login_type == 1 else "manager")
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

async def naver_login(naver_token):
    try:
        headers = {'Authorization': f'Bearer {naver_token}'}
        response = requests.get('https://openapi.naver.com/v1/nid/me', headers=headers)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        user_info = response.json()['response']

        oauth_user_info = OAuthUserInfo(
                id = user_info["id"],
                nickname = user_info["nickname"],
                email = user_info.get("email") # 이메일 없을수도 있어서 get 사용
            )
        user = await get_user(naver_id=oauth_user_info.id)

        if not user:
          user = await create_user(naver_id=oauth_user_info.id, name=oauth_user_info.nickname, email=oauth_user_info.email)
          if not user:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
        token = generate_jwt(user.userid, "user")
        return {"access_token": token, "token_type": "bearer"}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Naver API Error: {e}")
    except KeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Naver response")

async def kakao_login(kakao_token):
    try:
        headers = {'Authorization': f'Bearer {kakao_token}'}
        response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
        response.raise_for_status()
        user_info = response.json()

        oauth_user_info = OAuthUserInfo(
                id = str(user_info["id"]),
                nickname = user_info.get("properties").get("nickname"), # 닉네임 경로가 다를수있음
                email = user_info.get("kakao_account").get("email") # 이메일 경로가 다를수있음
            )

        user = await get_user(kakao_id=oauth_user_info.id)

        if not user:
            user = await create_user(kakao_id=oauth_user_info.id, name=oauth_user_info.nickname, email = oauth_user_info.email)
            if not user:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")

        token = generate_jwt(user.userid, "user")
        return {"access_token": token, "token_type": "bearer"}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Kakao API Error: {e}")
    except KeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Kakao response")