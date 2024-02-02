import pytest
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.main import app
from app.models import *
from fastapi.testclient import TestClient
from .data import menu_data, submenu_data, dish_data


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
client = TestClient(app)


@pytest.fixture(autouse=True, scope='session')
def create_test_database():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="module")
def db():
    """I don't know for what is it, but without it nothing works"""
    connection = engine_test.connect()
    session = TestSession(bind=connection)

    yield session

    session.close()


@pytest.fixture(autouse=False, scope='function')
def setup_test_database(db):
    db_menu = Menu(
        id=menu_data['id'],
        title=menu_data['title'],
        description=menu_data['description']
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)

    db_submenu = SubMenu(
        id=submenu_data['id'],
        title=submenu_data['title'],
        description=submenu_data['description'],
        id_menu=db_menu.id
    )
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)

    db_dish = Dish(
        id=dish_data['id'],
        title=dish_data['title'],
        description=dish_data['description'],
        price=dish_data['price'],
        id_submenu=db_submenu.id
    )
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)

    yield db

    db.query(Dish).delete()
    db.query(SubMenu).delete()
    db.query(Menu).delete()
    db.commit()
