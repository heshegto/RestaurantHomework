from typing import AsyncGenerator
from uuid import UUID

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.databases.models import SubMenu

from .conftest import async_session_maker
from .data import menu_data, new_submenu_data, submenu_data, updated_submenu_data
from .reverse import reverse


@pytest.mark.asyncio
async def test_create_submenu(
        setup_test_database,
        ac: AsyncGenerator[AsyncClient, None],
        new_data: dict[str, str] = new_submenu_data
) -> None:
    response = await ac.post(reverse('create_submenu').format(target_menu_id=menu_data['id']), json=new_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert type(UUID(data['id'])) == UUID
    assert data['title'] == new_data['title']
    assert data['description'] == new_data['description']

    query = select(SubMenu).where(SubMenu.id == UUID(data['id']))
    async with async_session_maker() as session:
        data_from_db = (await session.execute(query)).scalar_one()
    assert data_from_db.id == UUID(data['id'])
    assert data_from_db.title == new_data['title']
    assert data_from_db.description == new_data['description']


@pytest.mark.asyncio
async def test_read_submenu_by_id(setup_test_database, ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_submenu_by_id').format(
        target_menu_id=menu_data['id'],
        target_submenu_id=submenu_data['id']
    ))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == submenu_data['id']
    assert data['title'] == submenu_data['title']
    assert data['description'] == submenu_data['description']


@pytest.mark.asyncio
async def test_read_submenu_by_id_not_found(ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_submenu_by_id').format(
        target_menu_id=menu_data['id'],
        target_submenu_id=submenu_data['id']
    ))
    assert response.status_code == 404
    assert response.json()
    assert response.json()['detail'] == 'submenu not found'


@pytest.mark.asyncio
async def test_read_submenus(setup_test_database, ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_submenus').format(target_menu_id=menu_data['id']))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data != []
    assert UUID(data[0]['id']) == submenu_data['id']
    assert data[0]['title'] == submenu_data['title']
    assert data[0]['description'] == submenu_data['description']


@pytest.mark.asyncio
async def test_read_submenus_empty(ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_submenus').format(target_menu_id=menu_data['id']))
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_update_submenu(
        setup_test_database,
        ac: AsyncGenerator[AsyncClient, None],
        updated_data: dict[str, str] = updated_submenu_data
) -> None:
    response = await ac.patch(
        reverse('update_submenu').format(
            target_menu_id=menu_data['id'],
            target_submenu_id=submenu_data['id']
        ),
        json=updated_data
    )
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == submenu_data['id']
    assert data['title'] == updated_data['title']
    assert data['description'] == updated_data['description']

    query = select(SubMenu).where(SubMenu.id == submenu_data['id'])
    async with async_session_maker() as session:
        data_from_db = (await session.execute(query)).scalar()
    assert data_from_db.id == submenu_data['id']
    assert data_from_db.title == updated_data['title']
    assert data_from_db.description == updated_data['description']


@pytest.mark.asyncio
async def test_delete_submenu(setup_test_database, ac: AsyncGenerator[AsyncClient, None]) -> None:
    query = select(SubMenu).where(SubMenu.id == submenu_data['id'])
    async with async_session_maker() as session:
        flag_item = (await session.execute(query)).scalar()
    assert flag_item is not None

    response = await ac.delete(reverse('update_submenu').format(
        target_menu_id=menu_data['id'],
        target_submenu_id=submenu_data['id']
    ))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == submenu_data['id']
    assert data['title'] == submenu_data['title']
    assert data['description'] == submenu_data['description']

    query = select(SubMenu).where(SubMenu.id == submenu_data['id'])
    async with async_session_maker() as session:
        flag_item = (await session.execute(query)).scalar()
    assert flag_item is None
