from typing import List

from sqlalchemy import select

from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room
    async def get_all(self, hotel_id: int) -> List[Room]:
        query = select(RoomsORM).filter_by(hotel_id=hotel_id)

        result = await self.session.execute(query)
        return [Room.model_validate(room, from_attributes=True) for room in result.scalars().all()]