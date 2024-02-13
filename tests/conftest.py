import os
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from redis import Redis

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, delete

from app.databases.db.database import get_db
from app.main import app
from typing import Generator

import asyncio

from app.databases.cache.cache import get_redis
from app.databases.db.database import Base
from app.databases.models import Dish, Menu, SubMenu

from .data import dish_data, menu_data, submenu_data
from sqlalchemy.pool import NullPool

TEST_DATABASE_URL = 'postgresql+asyncpg://{}:{}@{}/{}'.format(
    os.getenv('POSTGRES_DB_USER', 'postgres'),
    os.getenv('POSTGRES_DB_PASSWORD', '5875'),
    os.getenv('POSTGRES_DB_CONTAINER_NAME_FOR_TESTS', 'localhost:5432'),
    os.getenv('POSTGRES_DB_FOR_TESTS', 'postgres')
)

TEST_REDIS_URL = 'redis://{name}:{port}'.format(
    name=os.getenv('REDIS_NAME_FOR_TESTS', 'redis'),
    port=os.getenv('REDIS_PORT_FOR_TESTS', '6379')
)

pytest_plugins = ('pytest_asyncio',)
engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_db] = override_get_session


@pytest_asyncio.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True, scope='session')
async def create_test_database() -> Generator:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        yield ac


@pytest_asyncio.fixture(autouse=False, scope='function')
async def setup_test_database(red: Redis = get_redis()) -> None:
    query1 = insert(Menu).values(
        id=menu_data['id'],
        title=menu_data['title'],
        description=menu_data['description']
    )

    query2 = insert(SubMenu).values(
        id=submenu_data['id'],
        title=submenu_data['title'],
        description=submenu_data['description'],
        id_parent=menu_data['id']
    )

    query3 = insert(Dish).values(
        id=dish_data['id'],
        title=dish_data['title'],
        description=dish_data['description'],
        price=dish_data['price'],
        id_parent=submenu_data['id']
    )
    async with async_session_maker() as session:
        await session.execute(query1)
        await session.execute(query2)
        await session.execute(query3)
        await session.commit()

    yield

    red.flushdb()
    red.close()

    async with async_session_maker() as session:
        await session.execute(delete(Dish))
        await session.execute(delete(SubMenu))
        await session.execute(delete(Menu))
        await session.commit()
