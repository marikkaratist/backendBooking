from datetime import date
from fastapi import APIRouter, Query, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2023-12-15"),
    date_to: date = Query(example="2023-12-20"),
):
    hotels = await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )
    return {"status": 200, "data": hotels}

@router.get("/{hotel_id}")
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Deluxe Cloud", "location": "Сочи, ул.Моря 3"},
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Luxury", "location": "Дубай, ул. Шейха 8"},
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": 201, "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).update_hotel(hotel_id, hotel_data)
    return {"status": 204}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление",
    description="<h1> Здесь можно частично обновлять данные. Можно обновить title, можно обновить name. А можно всё сразу. </h1>",
)
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelService(db).patch_hotel(hotel_id, hotel_data)
    return {"status": 204}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": 204}
