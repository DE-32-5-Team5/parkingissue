from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from models.register import RequestUserSchema, RequestManagerSchema
from services.register import (
    check_user_id_service,
    check_manager_id_service,
    check_manager_phone_service,
    user_register_service,
    manager_register_service,
)

r_register = APIRouter(
    prefix="/api",
    tags=["register"]
)

# 회원가입 폼 - ID 체크 / 개인
@r_register.post("/users/check")
async def user_check_id(request: RequestUserSchema = Depends()):
    if not check_user_id_service(request.User.id):
        raise HTTPException(status_code=400, detail="user_id isn't Unique")
    return {"status": 200, "detail": "user_id is Unique"}

# 회원가입 폼 - ID 체크 / 기업
@r_register.post("/company/check/id")
async def manager_check_id(request: RequestManagerSchema = Depends()):
    if not check_manager_id_service(request.Manager.id):
        raise HTTPException(status_code=400, detail="manager_id isn't Unique")
    return {"status": 200, "detail": "manager_id is Unique"}

# 회원가입 폼 - 전화번호 체크 / 기업
@r_register.post("/company/check/phone")
async def user_register(request: RequestManagerSchema = Depends()):
    if not check_manager_phone_service(request.Manager.phone):
        raise HTTPException(status_code=400, detail="manager_phone isn't Unique")
    return {"status": 200, "detail": "manager_phone is Unique"}

# 회원가입 폼 - 저장 / 개인
@r_register.post("/users/register")
async def user_register(request: RequestUserSchema = Depends()):
    if not check_user_id_service(request.User.id):
        raise HTTPException(status_code=400, detail="user_id isn't Unique")
    if user_register_service(request.User):
        return {"status": 200, "detail": "user registering is success"}
    return JSONResponse(content={"status": 404, "detail": "user registering is failed"}, status_code=404)

# 회원가입 폼 - 저장 / 기업
@r_register.post("/company/register")
async def manager_check_id(request: RequestManagerSchema = Depends()):
    if not check_manager_id_service(request.Manager.id):
        raise HTTPException(status_code=400, detail="manager_id isn't Unique")
    if manager_register_service(request.Manager):
        return {"status": 200, "detail": "manager registering is success"}
    return JSONResponse(content={"status": 404, "detail": "company registering is failed"}, status_code=404)