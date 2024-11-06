from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body(openapi_examples={
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
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": 201, "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(hotel_id: int, room_id: int, db: DBDep, room_data: RoomAddRequest = Body(openapi_examples={
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
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": 204}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_room(hotel_id: int, room_id: int, db: DBDep, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id)
    await db.commit()
    return {"status": 204}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": 204}
