from typing import Optional
from fastapi import APIRouter, Query, Body
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Morocco", "name": "morocco"},
    {"id": 4, "title": "Altai", "name": "altai"},
    {"id": 5, "title": "Anapa", "name": "anapa"},
    {"id": 6, "title": "Nebraska", "name": "nebraska"},
    {"id": 7, "title": "Vancouver", "name": "vancouver"},
    {"id": 8, "title": "Grand", "name": "grand"},
]


@router.get("/")
def get_hotels(
        id: Optional[int] = Query(None, description="Айдишник"),
        title: Optional[str] = Query(None, description="Название отеля"),
        page: Optional[int] = Query(1, description="Страница"),
        per_page: Optional[int] = Query(2, description="Количество записей на странице")

):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        elif title and hotel["title"] != title:
            continue
        else:
            hotels_.append(hotel)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_hotels = hotels_[start:end]
        return paginated_hotels


@router.post("/")
def create_hotels(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Sochi",
        "name": "отель у моря"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Ararat",
        "name": "прекрасный отель"
    }},
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status": 201}


@router.put("/{hotel_id}")
def update_hotels(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
    return {"status": 200}


@router.patch("/{hotel_id}")
def patch_hotels(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
    return {"status": 200}


@router.delete("/{hotel_id}")
def delete_hotels(
        hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": 204}
