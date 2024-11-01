from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms():
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all()


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post("/")
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
            "description": "Супер комфортный роскошный отель с двумя санузлами",
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
