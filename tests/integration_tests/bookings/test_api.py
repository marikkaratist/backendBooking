

async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2024-11-10",
            "date_to": "2024-11-20"
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert "data" in res
    assert isinstance(res, dict)
