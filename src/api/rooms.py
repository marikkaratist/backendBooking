from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import HotelNotFoundHTTPException, RoomNotFoundHTTPException, HotelNotFoundException, RoomNotFoundException
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest, Room
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
@cache(expire=10)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2023-12-10"),
    date_to: date = Query(example="2023-12-15"),
):
    rooms = await RoomService(db).get_filtered_by_time(
        hotel_id,
        date_from,
        date_to,
    )
    return {"status": 200, "data": rooms}


@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=10)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        room = await RoomService(db).get_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": 200, "data": room}


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Basic",
                "value": {
                    "title": "Basic room",
                    "description": "Очень комфортный уютный номер с одним санузлом",
                    "price": 500,
                    "quantity": 3,
                    "facilities_ids": [1, 2],
                },
            },
            "2": {
                "summary": "Deluxe",
                "value": {
                    "title": "Deluxe room",
                    "description": "Супер комфортный роскошный номер с двумя санузлами",
                    "price": 1500,
                    "quantity": 4,
                },
            },
        }
    ),
):
    try:
        room = await RoomService(db).add_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Basic",
                "value": {
                    "title": "Basic room",
                    "description": "Лайтовый номер по скидке",
                    "price": 250,
                    "quantity": 3,
                    "facilities_ids": [],
                },
            },
            "2": {
                "summary": "Deluxe",
                "value": {
                    "title": "Deluxe room",
                    "description": "Достаточно дороговатый номер по сравнению даже с дорогими номерами",
                    "price": 2500,
                    "quantity": 6,
                    "facilities_ids": [],
                },
            },
        }
    ),
):
    await RoomService(db).update_room(hotel_id, room_id, room_data)
    return {"status": 204}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(hotel_id: int, room_id: int, db: DBDep, room_data: RoomPatchRequest):
    await RoomService(db).patch_room(hotel_id, room_id, room_data)
    return {"status": 204}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": 204}
