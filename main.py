from typing import Optional

from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]


@app.get("/hotels")
def get_hotels(
        id: Optional[int] = Query(None, description="Айдишник"),
        title: Optional[str] = Query(None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        elif title and hotel["title"] != title:
            continue
        else:
            hotels_.append(hotel)
    return hotels_


@app.post("/hotels")
def create_hotels(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": 201}


@app.put("/hotels/{hotel_id}")
def update_hotels(
        hotel_id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True)

):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
    return {"status": 200}


@app.patch("/hotels/{hotel_id}")
def patch_hotels(
        hotel_id: int,
        title: Optional[str] = Body(None, embed=True),
        name: Optional[str] = Body(None, embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            elif name is not None:
                hotel["name"] = name
    return {"status": 200}


@app.delete("/hotels/{hotel_id}")
def delete_hotels(
        hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": 204}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
