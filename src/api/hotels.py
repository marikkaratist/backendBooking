from fastapi import APIRouter, Query, Body

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),

):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=(pagination.page - 1) * per_page
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("/")
async def create_hotels(hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Deluxe Cloud",
        "location": "Сочи, ул.Моря 3"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Luxury",
        "location": "Дубай, ул. Шейха 8"
    }},
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": 201, "data": hotel}


@router.put("/{hotel_id}")
async def update_hotels(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": 201}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление",
    description="<h1> Здесь можно частично обновлять данные. Можно обновить title, можно обновить name. А можно всё сразу. </h1>"
)
async def patch_hotels(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": 204}


@router.delete("/{hotel_id}")
async def delete_hotels(
        hotel_id: int
):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": 204}
