async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_post_facilities(ac):
    facility_title = "Душ"
    response = await ac.post("/facilities", json={"title": facility_title})
    res = response.json()
    assert response.status_code == 200
    assert res["data"]["title"] == facility_title
    assert "data" in res
    assert isinstance(res, dict)
