from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/")
@cache(expire=10)
async def get_facilities(db: DBDep):
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

    test_task.delay()

    return {"status": 201, "data": facility}
