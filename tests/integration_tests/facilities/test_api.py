

async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200

async def test_post_facility(ac):
    response = await ac.post(
        "/facilities",
        json={
            "title": "Душ"
        }
    )
    assert response.status_code == 200