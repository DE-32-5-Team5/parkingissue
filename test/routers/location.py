from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..services.location import (
    create_item_service,
    receive_location_service,
    frontget_service,
    get_park_info_service,
    get_related_data_service,
    get_click_search_service,
)
from ..models.location import Location, FromSpark

router = APIRouter(
    prefix="/api",
    tags=["location"]
)

@router.post("/location")
async def create_item(location: Location = Depends()):
    return await create_item_service(location)

@router.post("/getlocation")
async def receive_location(sparkdata: list[FromSpark] = Depends()):
    if not sparkdata:
        raise HTTPException(status_code=400, detail="Empty JSON data")
    return await receive_location_service(sparkdata)

@router.get("/frontget/")
async def frontget():
    return await frontget_service()

@router.get("/getParkInfo")
async def get_park_info(parkid: str):
    try:
        park_info = await get_park_info_service(parkid)
        if not park_info:
            raise HTTPException(status_code=404, detail="Park not found")
        return park_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getRelated")
async def get_related_data(text: str):
    result = await get_related_data_service(text)
    if result:
        dic = {}
        for i in result:
            for key, value in i.items():
                if key not in dic:
                    dic[key] = [value]
                else:
                    dic[key].append(value)
        return result

@router.get("/getClickSearch")
async def get_click_search(txt: str):
    return await get_click_search_service(txt)