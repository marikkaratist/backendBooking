from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)

        return result.scalars().one()

    async def edit(self, id: int, **filter_by):
        edit_data_stmt = update(self.model).filter(self.model.id == id).values(**filter_by)
        result = await self.session.execute(edit_data_stmt)

        return result

    async def delete(self, id: int):
        delete_data_stmt = delete(self.model).filter(self.model.id == id)
        result = await self.session.execute(delete_data_stmt)

        return result
