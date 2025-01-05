from datetime import date
from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2024, month=3, day=10),
        date_to=date(year=2024, month=3, day=20),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.user_id == new_booking.user_id
    assert booking.room_id == new_booking.room_id
    assert booking.price == 100
    # а еще можно вот так разом сравнить все параметры
    assert booking.model_dump(exclude={"id"}) == booking_data.model_dump()

    updated_date = date(year=2024, month=3, day=10)
    update_booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2024, month=3, day=10),
        date_to=updated_date,
        price=150,
    )
    await db.bookings.edit(update_booking_data, id=booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == updated_date

    await db.bookings.delete(user_id=user_id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
