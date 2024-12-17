from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from login.services.user_services import get_user_by_id, get_all_users, create_user
from login.models.user_info import UserInfo, UserInfoCreate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserInfoCreate):
    return await create_user(user)

@router.get("/{user_id}", response_model=UserInfo)
async def read_user(user_id: str):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserInfo])
async def read_users():
    users = await get_all_users()
    return users