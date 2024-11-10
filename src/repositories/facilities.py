from src.models.facilities import FacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility