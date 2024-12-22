from fastapi import APIRouter, Depends
from ..models.hotplace import Location, RequestHotplaceSchemaq  # 필요한 모델 import
from ..services.hotplace import (
    hotplace_default_list_service,
    hotplace_ongoing_list_service,
    hotplace_upcoming_list_service,
    # hotplace_adress_list_service,  # 주석 처리
    hotplace_content_info_service
)

router = APIRouter(
    prefix="/api/hotplace",
    tags=["hotplace"]
)

# 핫플레이스 게시글 리스트 요청 (가까운 순)
@router.post("/list/default")
async def hotplace_default_list(location: Location = Depends()):
    return await hotplace_default_list_service(location)

# 핫플레이스 게시글 리스트 요청 (진행중이며, 끝나는 일자가 가까운 순)
@router.post("/list/ongoing")
async def hotplace_ongoing_list():
    return await hotplace_ongoing_list_service()

# 핫플레이스 게시글 리스트 요청 (아직 시작안함, 끝나는 일자가 가까운 순)
@router.post("/list/upcoming")
async def hotplace_upcoming_list():
    return await hotplace_upcoming_list_service()

# 핫플레이스 게시글 리스트 요청 (지역분류, 끝나는 일자가 가까운 순)
# @app.post("/api/hotplace/list/adress")
# async def hotplace_adress_list(resion: str):
#     return await hotplace_adress_list_service(resion)

# 핫플레이스 게시글 내용 요청 (상세정보)
@router.post("/content")
async def hotplace_content_info(contentid: str):  # contentid 매개변수 추가
    return await hotplace_content_info_service(contentid)