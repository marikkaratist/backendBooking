from sqlalchemy import select, func, insert

from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
        query = select(HotelsORM)
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
        if title:
            query = query.filter(HotelsORM.title.ilike(f"%{title}%"))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self, location, title):
        add_hotel_stmt = insert(self.model).values({
            "location": location,
            "title": title
        })
        result = await self.session.execute(add_hotel_stmt)
        await self.session.commit()
        return result
