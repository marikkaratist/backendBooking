from dns.e164 import query
from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
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
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
        return {"status": 201, "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(hotel_id: int, room_id: int, room_data: RoomAddRequest = Body(openapi_examples={
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
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
    return {"status": 204}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": 204}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": 204}
