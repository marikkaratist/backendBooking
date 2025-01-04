from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
@cache(expire=10)
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
@cache(expire=10)
async def get_me(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def create_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest = Body(
            openapi_examples={
                "1": {
                    "summary": "Бронирование №1",
                    "value": {"room_id": 1, "date_from": "2023-12-10", "date_to": "2023-12-15"},
                },
                "2": {
                    "summary": "Бронирование №2",
                    "value": {"room_id": 2, "date_from": "2023-12-22", "date_to": "2023-12-28"},
                },
            }
        ),
):
    try:
        booking = await BookingService(db).create_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}
