from fastapi import APIRouter, Query, Body

from dependencies import PaginationDep
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
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),

):
    hotels_ = []
    for hotel in hotels:
        if id is not None and hotel["id"] != id:
            continue
        elif title is not None and hotel["title"] != title:
            continue
        else:
            hotels_.append(hotel)
    if pagination.page and pagination.per_page:
        start = (pagination.page - 1) * pagination.per_page
        end = start + pagination.per_page
        paginated_hotels = hotels_[start:end]
        return paginated_hotels
    return hotels_


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


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление",
    description="<h1> Здесь можно частично обновлять данные. Можно обновить title, можно обновить name. А можно всё сразу. </h1>"
)
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
