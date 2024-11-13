from datetime import date
from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2023-12-10"),
        date_to: date = Query(example="2023-12-15")
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Basic", "value": {
            "title": "Basic room",
            "description": "Очень комфортный уютный номер с одним санузлом",
            "price": 500,
            "quantity": 3,
            "facilities_ids": [
                1, 2
            ]
        }
    },
    "2": {
        "summary": "Deluxe", "value": {
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
    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": 201, "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(hotel_id: int, room_id: int, db: DBDep, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Basic", "value": {
            "title": "Basic room",
            "description": "Лайтовый номер по скидке",
            "price": 250,
            "quantity": 3,
            "facilities_ids": []
        }
    },
    "2": {
        "summary": "Deluxe", "value": {
            "title": "Deluxe room",
            "description": "Достаточно дороговатый номер по сравнению даже с дорогими номерами",
            "price": 2500,
            "quantity": 6,
            "facilities_ids": []
        }
    }
})
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": 204}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_room(hotel_id: int, room_id: int, db: DBDep, room_data: RoomPatchRequest):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])
    await db.commit()
    return {"status": 204}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": 204}
