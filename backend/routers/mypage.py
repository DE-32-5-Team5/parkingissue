from fastapi import APIRouter, Depends, HTTPException, status
"""
from models.mypage import ChangePasswordRequest
from services.mypage import change_password_service
"""

router = APIRouter(
    prefix="/api",
    tags=["mypage"]
)

"""
@router.post("/change-password/")
async def change_password(
    request: ChangePasswordRequest, 
    db: Session = Depends(get_db)
):
    try: 
        return await change_password_service(request, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"비밀번호 변경 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="비밀번호 변경 중 오류 발생")
"""