# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware


# # 데이터베이스 세션 연결 및 모델 import
# from .database import get_db
# from .models import FestivalInfo # type: ignore

# app = FastAPI()

# # CORS 설정
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 모든 출처(origin)에서의 요청을 허용. 특정 도메인만 허용하려면 목록에 도메인 추가.
#     allow_credentials=True,
#     allow_methods=["*"],  # 모든 HTTP 메소드(GET, POST 등)를 허용
#     allow_headers=["*"],  # 모든 헤더를 허용
# )

# class ChangePasswordRequest(BaseModel):
#     current_password: str
#     new_password: str
#     confirm_password: str


# @app.post("/change-password/")
# async def change_password(request: ChangePasswordRequest, db: Session = Depends(get_db)):
#     # 로그인된 사용자 가져오기 (예시: 사용자 ID는 세션에서 가져온다고 가정)
#     user = db.query(FestivalInfo).filter(FestivalInfo.managerid == 1).first()  # 예시로 userid = 1

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # 1. 현재 비밀번호 확인
#     if user.password != request.current_password:
#         raise HTTPException(status_code=400, detail="현재 비밀번호가 틀립니다.")  # 현재 비밀번호 불일치 시 오류
        

#     # 2. 새 비밀번호와 새 비밀번호 확인이 일치하는지 확인
#     if request.new_password != request.confirm_password:
#         raise HTTPException(status_code=400, detail="새 비밀번호와 비밀번호 확인이 일치하지 않습니다.")  # 새 비밀번호 불일치 시 오류

#     # 3. DB에서 비밀번호 업데이트 (해시화 없이 평문으로 저장)
#     user.password = request.new_password  # 해시화 없이 평문으로 비밀번호 업데이트
#     db.commit()  # 변경사항 커밋

#     return {"message": "비밀번호 변경 완료"}
