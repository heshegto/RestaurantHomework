import os
from typing import Iterator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://{}:{}@{}/{}'.format(
    os.getenv('POSTGRES_DB_USER', 'postgres'),
    os.getenv('POSTGRES_DB_PASSWORD', '5875'),
    os.getenv('POSTGRES_DB_CONTAINER_NAME', 'localhost:5432'),
    os.getenv('POSTGRES_DB', 'postgres')
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> Iterator[AsyncSession]:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
