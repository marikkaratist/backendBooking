async def test_hotels(ac):
    response = await ac.get("/hotels", params={"date_from": "2024-11-10", "date_to": "2024-11-20"})
    print(f"{response.json()=}")

    assert response.status_code == 200
