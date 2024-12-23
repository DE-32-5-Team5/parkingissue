from fastapi import APIRouter, File, UploadFile
from models.event import FestivalInfo
from services.event import register_event_service

router = APIRouter(
    prefix = "/api/event",
    tags = ["event"]
)

"""
    라우터로 전환하면서 변경점 안내
    백엔드 API 엔드포인트 위치가 달라졌습니다.
    기존 : /event-registration
    변경 : /api/event/registration

    
"""

@router.post("/registration")
async def register_event(festival_info: FestivalInfo):
    return await register_event_service(festival_info)
