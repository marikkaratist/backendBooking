from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("/")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()

@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)

@router.post("/")
async def create_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Бронирование №1", "value": {
            "room_id": 1,
            "date_from": "2023-12-10",
            "date_to": "2023-12-15"
        }
    },
    "2": {
        "summary": "Бронирование №2", "value": {
            "room_id": 2,
            "date_from": "2023-12-22",
            "date_to": "2023-12-28"
        }
    }
})
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": 201, "data": booking}