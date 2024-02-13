from uuid import UUID
import pytest
from sqlalchemy import select
from typing import AsyncGenerator

from app.databases.models import Dish
from httpx import AsyncClient

from .data import dish_data, menu_data, new_dish_data, submenu_data, updated_dish_data
from .reverse import reverse
from .conftest import async_session_maker


@pytest.mark.asyncio
async def test_create_dish(
        setup_test_database,
        ac: AsyncGenerator[AsyncClient, None],
        new_data: dict[str, str] = new_dish_data
) -> None:
    response = await ac.post(
        reverse('create_dish').format(
            target_menu_id=menu_data['id'],
            target_submenu_id=submenu_data['id']
        ),
        json=new_data
    )
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert type(UUID(data['id'])) == UUID
    assert data['title'] == new_data['title']
    assert data['description'] == new_data['description']

    query = select(Dish).where(Dish.id == UUID(data['id']))
    async with async_session_maker() as session:
        data_from_db = (await session.execute(query)).scalar_one()
    assert data_from_db.id == UUID(data['id'])
    assert data_from_db.title == new_data['title']
    assert data_from_db.description == new_data['description']


@pytest.mark.asyncio
async def test_read_dish_by_id(setup_test_database, ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_dish_by_id').format(
        target_menu_id=menu_data['id'],
        target_submenu_id=submenu_data['id'],
        target_dish_id=dish_data['id']
    ))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == dish_data['id']
    assert data['title'] == dish_data['title']
    assert data['description'] == dish_data['description']


@pytest.mark.asyncio
async def test_read_dish_by_id_not_found(ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_dish_by_id').format(
        target_menu_id=menu_data['id'],
        target_submenu_id=submenu_data['id'],
        target_dish_id=dish_data['id']
    ))
    assert response.status_code == 404
    assert response.json()
    assert response.json()['detail'] == 'dish not found'


@pytest.mark.asyncio
async def test_read_dishes(setup_test_database, ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_dishes').format(
        target_menu_id=menu_data['id'],
        target_submenu_id=submenu_data['id'],
    ))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data != []
    assert UUID(data[0]['id']) == dish_data['id']
    assert data[0]['title'] == dish_data['title']
    assert data[0]['description'] == dish_data['description']


@pytest.mark.asyncio
async def test_read_dish_empty(ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_dishes').format(
        target_menu_id=menu_data['id'],
        target_submenu_id=submenu_data['id'],
    ))
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_update_dish(
        setup_test_database,
        ac: AsyncGenerator[AsyncClient, None],
        updated_data: dict[str, str] = updated_dish_data
) -> None:
    response = await ac.patch(
        reverse('update_dish').format(
            target_menu_id=menu_data['id'],
            target_submenu_id=submenu_data['id'],
            target_dish_id=dish_data['id']
        ),
        json=updated_data
    )
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == dish_data['id']
    assert data['title'] == updated_data['title']
    assert data['description'] == updated_data['description']

    query = select(Dish).where(Dish.id == dish_data['id'])
    async with async_session_maker() as session:
        data_from_db = (await session.execute(query)).scalar()
    assert data_from_db.id == dish_data['id']
    assert data_from_db.title == updated_data['title']
    assert data_from_db.description == updated_data['description']


@pytest.mark.asyncio
async def test_delete_dish(setup_test_database, ac: AsyncGenerator[AsyncClient, None]) -> None:
    query = select(Dish).where(Dish.id == dish_data['id'])
    async with async_session_maker() as session:
        flag_item = (await session.execute(query)).scalar()
    assert flag_item is not None

    response = await ac.delete(reverse('update_dish').format(
        target_menu_id=menu_data['id'],
        target_submenu_id=submenu_data['id'],
        target_dish_id=dish_data['id']
    ))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == dish_data['id']
    assert data['title'] == dish_data['title']
    assert data['description'] == dish_data['description']

    query = select(Dish).where(Dish.id == dish_data['id'])
    async with async_session_maker() as session:
        flag_item = (await session.execute(query)).scalar()
    assert flag_item is None
