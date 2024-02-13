from uuid import UUID
import pytest

from typing import AsyncGenerator

from httpx import AsyncClient
from .conftest import ac
from .data import dish_data, menu_data, submenu_data
from .reverse import reverse


@pytest.mark.asyncio
async def test_read_everything(setup_test_database, ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_everything'))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data != []
    assert UUID(data[0]['id']) == menu_data['id']
    assert data[0]['title'] == menu_data['title']
    assert data[0]['description'] == menu_data['description']

    assert data[0]['child_menu'][0] != []
    assert UUID(data[0]['child_menu'][0]['id']) == submenu_data['id']
    assert data[0]['child_menu'][0]['title'] == submenu_data['title']
    assert data[0]['child_menu'][0]['description'] == submenu_data['description']

    assert data[0]['child_menu'][0]['dish'][0] != []
    assert UUID(data[0]['child_menu'][0]['dish'][0]['id']) == dish_data['id']
    assert data[0]['child_menu'][0]['dish'][0]['title'] == dish_data['title']
    assert data[0]['child_menu'][0]['dish'][0]['description'] == dish_data['description']
    assert data[0]['child_menu'][0]['dish'][0]['price'] == dish_data['price']


@pytest.mark.asyncio
async def test_read_everything_empty(ac: AsyncGenerator[AsyncClient, None]) -> None:
    response = await ac.get(reverse('read_everything'))
    assert response.status_code == 200
    assert response.json() == []
