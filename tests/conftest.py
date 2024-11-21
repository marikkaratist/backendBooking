import json
import os

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *
from src.models.hotels import HotelsORM


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine_null_pool) as session:
        with open(os.path.join("tests", "mock_hotels.json"), "r") as file:
            data = json.load(file)

        hotels = [HotelsORM(**hotel) for hotel in data]
        session.add_all(hotels)
        await session.commit()

        with open(os.path.join("tests", "mock_rooms.json"), "r") as file:
            data = json.load(file)

        rooms = [RoomsORM(**room) for room in data]
        session.add_all(rooms)
        await session.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test123") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "12345"
            }
        )
