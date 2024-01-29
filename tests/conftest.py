import pytest
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.main import app
from app.models import Base
from fastapi.testclient import TestClient
# from fastapi import FastAPI
# app = FastAPI()


TEST_DATABASE_URL = 'postgresql://{}:{}@{}/{}'.format(
    os.getenv('POSTGRES_DB_USER', 'postgres'),
    os.getenv('POSTGRES_DB_PASSWORD', ''),
    os.getenv('POSTGRES_DB_CONTAINER_NAME_FOR_TESTS', 'postgres'),
    os.getenv('POSTGRES_DB_FOR_TESTS', 'postgres')
)

engine_test = create_engine(TEST_DATABASE_URL)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()



app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope='session')
def create_test_database():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


client = TestClient(app)
