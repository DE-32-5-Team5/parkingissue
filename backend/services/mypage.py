from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.mypage import ChangePasswordRequest
from ..models.userinfo import UserInfo

async def change_password_service(request: ChangePasswordRequest, db: Session):
    # 로그인된 사용자 가져오기 (예시: 사용자 ID는 세션에서 가져온다고 가정)
    user = db.query(UserInfo).filter(UserInfo.userid == 1).first()  # 예시로 userid = 1

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 1. 현재 비밀번호 확인
    if user.password != request.current_password:  # 평문 비교 (주의: 실제로는 해싱된 비밀번호를 비교해야 함)
        raise HTTPException(status_code=400, detail="현재 비밀번호가 틀립니다.")

    # 2. 새 비밀번호와 새 비밀번호 확인이 일치하는지 확인
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=400, detail="새 비밀번호와 비밀번호 확인이 일치하지 않습니다.")

    # 3. DB에서 비밀번호 업데이트
    user.password = request.new_password  # 평문으로 저장 (주의: 실제로는 해싱된 비밀번호를 저장해야 함)
    db.commit()

    return {"message": "비밀번호 변경 완료"}