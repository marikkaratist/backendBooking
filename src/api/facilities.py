from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/")
async def get_facilities(
        db: DBDep
):
    return await db.facilities.get_all()

@router.post("/")
async def add_facility(db: DBDep, facility_data: FacilityAdd = Body(openapi_examples={
    "1": {
        "summary": "Интернет", "value": {
            "title": "Бесплатный интернет"
        }
    },
    "2": {
        "summary": "Парковка", "value": {
            "title": "Парковка"
        }
    }
})
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": 201, "data": facility}