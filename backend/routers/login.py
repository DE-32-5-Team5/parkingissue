from fastapi import APIRouter, Header

from services.login import (
    login_personal_service,
    login_enterprise_service,
    login_naver_service,
    login_kakao_service,
    check_user_service,
    update_token_service,
)
from models.login import (
    PersonalLogin,
    EnterpriseLogin,
    NaverLogin,
    KakaoLogin,
)

"""
    Router : 라우터
    이곳에서는 요청이 들어올 엔드포인트를 저장해둔 다음, 해당 엔드포인트에서 실행할 함수(서비스)를 지정, 선언해두는 곳입니다.

    router = APIRouter(
        prefix = "당신의 요청 함수들을 모아두는 곳"
        tags = 태그
    )

    @router.post("prefix/요청할 곳")
    async def your_function():
        return await your_function_service()

    다음과 같이 작업해주시면 됩니다.
"""

router = APIRouter(
    prefix = "/api/login",
    tags = ["login"],
)

# idpw 일반회원 로그인
@router.post("/common/personal")
async def login_personal():
    return await login_personal_service(PersonalLogin)

# idpw 기업회원 로그인
@router.post("/common/enterprise")
async def login_enterprise():
    return await login_enterprise_service(EnterpriseLogin)

# 일반회원 네이버 간편로그인
@router.post("/simple/naver")
async def login_naver():
    return await login_naver_service(NaverLogin)

# 일반회원 카카오 간편로그인
@router.post("/simple/kakao")
async def login_kakao():
    return await login_kakao_service(KakaoLogin)

# 회원여부 검증
@router.post("/check/isuser")
async def check_isuser(token: str = Header(..., description="JWT 토큰")):
    return await check_user_service(token)

# 토큰 갱신 함수
@router.post("/check/updatetoken")
async def update_token(token: str = Header(..., description="JWT 토큰")):
    return await update_token_service(token)
                       
