from fastapi import HTTPException, status
import bcrypt
import os

from ..db import login_db
from .jwt_handler import create_jwt_token
from ..models.login import (
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
    conn = login_db()
    if not conn:
        # 데이터베이스 연결 오류
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")

    try:
        with conn.cursor() as cursor:
            # 1. 사용자 인증 (아이디, 비밀번호 확인) - 실제 인증 로직 구현
            sql = "SELECT user_id, user_pw FROM user_info WHERE id = %s"
            cursor.execute(sql, (personal_login.user_id,))
            user = cursor.fetchone()

            if not user or not bcrypt.checkpw(personal_login.user_pw.encode(), user['user_pw'].encode()):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # 2. JWT 토큰 생성
            access_token = create_jwt_token(user['uid'], secret_key)  # JWT secret key 설정

            return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print(f"로그인 처리 오류: {e}")
        raise HTTPException(status_code=500, detail="로그인 처리 오류")

    finally:
        conn.close()

async def login_enterprise_service(enterprise_login: EnterpriseLogin):
    """
        기업회원 id, pw 기반 로그인 시도시 작동하는 서비스
    """
    secret_key = os.getenv("JWT_LOGIN_ACCESS_KEY")
    conn = login_db()
    if not conn:
        # 데이터베이스 연결 오류
        raise HTTPException(status_code=500, detail="데이터베이스 연결 오류")

    try:
        with conn.cursor() as cursor:
            # 1. 사용자 인증 (아이디, 비밀번호 확인) - 실제 인증 로직 구현
            sql = "SELECT manager_id, manager_pw FROM manager_info WHERE manager_id = %s"
            cursor.execute(sql, (enterprise_login.manager_id,))
            user = cursor.fetchone()

            if not user or not bcrypt.checkpw(enterprise_login.manager_pw.encode(), user['manager_pw'].encode()):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # 2. JWT 토큰 생성
            access_token = create_jwt_token(user['mid'], secret_key)  # JWT secret key 설정

            return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print(f"로그인 처리 오류: {e}")
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
            access_token = create_jwt_token(user['uid'], secret_key)
            return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print(f"로그인 처리 오류: {e}")
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
            access_token = create_jwt_token(user['uid'], secret_key)
            return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print(f"로그인 처리 오류: {e}")
        raise HTTPException(status_code=500, detail="로그인 처리 오류")

    finally:
        conn.close()