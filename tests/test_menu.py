from uuid import UUID
import pytest
from sqlalchemy import select
from typing import AsyncGenerator

from app.databases.models import Menu
from httpx import AsyncClient

from .data import menu_data, new_menu_data, updated_menu_data
from .reverse import reverse
from .conftest import async_session_maker


@pytest.mark.asyncio
async def test_create_menu(
        setup_test_database,
        ac: AsyncGenerator[AsyncClient, None],
        new_data: dict[str, str] = new_menu_data
) -> None:
    response = await ac.post(reverse('create_menu'), json=new_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert type(UUID(data['id'])) is UUID
    assert data['title'] == new_data['title']
    assert data['description'] == new_data['description']

    query = select(Menu).where(Menu.id == UUID(data['id']))
    async with async_session_maker() as session:
        data_from_db = (await session.execute(query)).scalar_one()
    assert data_from_db.id == UUID(data['id'])
    assert data_from_db.title == new_data['title']
    assert data_from_db.description == new_data['description']


@pytest.mark.asyncio
async def test_read_menu_by_id(setup_test_database, ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_menu_by_id').format(target_menu_id=menu_data['id']))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == menu_data['id']
    assert data['title'] == menu_data['title']
    assert data['description'] == menu_data['description']


@pytest.mark.asyncio
async def test_read_menu_by_id_not_found(ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_menu_by_id').format(target_menu_id=menu_data['id']))
    assert response.status_code == 404
    assert response.json()
    assert response.json()['detail'] == 'menu not found'


@pytest.mark.asyncio
async def test_read_menus(setup_test_database, ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_menus'))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data != []
    assert UUID(data[0]['id']) == menu_data['id']
    assert data[0]['title'] == menu_data['title']
    assert data[0]['description'] == menu_data['description']


@pytest.mark.asyncio
async def test_read_menus_empty(ac: AsyncGenerator[AsyncClient, None]):
    response = await ac.get(reverse('read_menus'))
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_update_menu(
        setup_test_database,
        ac: AsyncGenerator[AsyncClient, None],
        updated_data: dict[str, str] = updated_menu_data
) -> None:
    response = await ac.patch(reverse('update_menu').format(target_menu_id=menu_data['id']), json=updated_data)
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == menu_data['id']
    assert data['title'] == updated_data['title']
    assert data['description'] == updated_data['description']

    query = select(Menu).where(Menu.id == menu_data['id'])
    async with async_session_maker() as session:
        data_from_db = (await session.execute(query)).scalar()
    assert data_from_db.id == menu_data['id']
    assert data_from_db.title == updated_data['title']
    assert data_from_db.description == updated_data['description']


@pytest.mark.asyncio
async def test_delete_menu(setup_test_database, ac: AsyncGenerator[AsyncClient, None]) -> None:
    query = select(Menu).where(Menu.id == menu_data['id'])
    async with async_session_maker() as session:
        flag_item = (await session.execute(query)).scalar()
    assert flag_item is not None

    response = await ac.delete(reverse('delete_menu').format(target_menu_id=menu_data['id']))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == menu_data['id']
    assert data['title'] == menu_data['title']
    assert data['description'] == menu_data['description']

    query = select(Menu).where(Menu.id == menu_data['id'])
    async with async_session_maker() as session:
        flag_item = (await session.execute(query)).scalar()
    assert flag_item is None
