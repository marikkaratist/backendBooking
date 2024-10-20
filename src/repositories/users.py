from sqlalchemy import select

from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.schemas.users import User


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = User

    async def user_exists(self, email: str) -> bool:
        query = select(self.model).filter(self.model.email == email)
        result = await self.session.execute(query)
        return result.scalars().one_or_none() is not None
