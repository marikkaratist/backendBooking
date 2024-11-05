from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPATCH

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post("/{hotel_id}/")
async def create_room(room_data: RoomAdd = Body(openapi_examples={
    "1": {
        "summary": "Basic", "value": {
            "hotel_id": "1",
            "title": "Basic room",
            "description": "Очень комфортный уютный номер с одним санузлом",
            "price": 500,
            "quantity": 3
        }
    },
    "2": {
        "summary": "Deluxe", "value": {
            "hotel_id": "2",
            "title": "Deluxe room",
            "description": "Супер комфортный роскошный номер с двумя санузлами",
            "price": 1500,
            "quantity": 4
        }
    }
})
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
        return {"status": 201, "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(room_id: int, room_data: RoomAdd = Body(openapi_examples={
    "1": {
        "summary": "Basic", "value": {
            "hotel_id": "1",
            "title": "Basic room",
            "description": "Лайтовый номер по скидке",
            "price": 250,
            "quantity": 3
        }
    },
    "2": {
        "summary": "Deluxe", "value": {
            "hotel_id": "2",
            "title": "Deluxe room",
            "description": "Достаточно дороговатый номер по сравнению даже с дорогими номерами",
            "price": 2500,
            "quantity": 6
        }
    }
})
                      ):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": 204}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_room(room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": 204}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": 204}
