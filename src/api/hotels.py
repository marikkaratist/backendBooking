from datetime import date
from fastapi import APIRouter, Query, Body, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundException, check_date_to_after_date_from, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatch, HotelAdd

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
    check_date_to_after_date_from(date_from, date_to)
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=(pagination.page - 1) * per_page,
    )


@router.get("/{hotel_id}")
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotels(
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": 201, "data": hotel}


@router.put("/{hotel_id}")
async def update_hotels(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": 201}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление",
    description="<h1> Здесь можно частично обновлять данные. Можно обновить title, можно обновить name. А можно всё сразу. </h1>",
)
async def patch_hotels(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": 204}


@router.delete("/{hotel_id}")
async def delete_hotels(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": 204}
