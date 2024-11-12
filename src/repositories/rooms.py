from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_from_booking
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date
    ):
        rooms_ids_to_get = rooms_ids_from_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_one_or_none_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRels.model_validate(model, from_attributes=True)