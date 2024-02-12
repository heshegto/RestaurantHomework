from uuid import UUID

from app.databases.models import SubMenu

from .conftest import client
from .data import menu_data, new_submenu_data, submenu_data, updated_submenu_data
from .reverse import reverse


def test_create_submenu(setup_test_database, new_data: dict[str, str] = new_submenu_data) -> None:
    response = client.post(reverse('create_submenu').format(target_menu_id=menu_data['id']), json=new_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert type(UUID(data['id'])) == UUID
    assert data['title'] == new_data['title']
    assert data['description'] == new_data['description']

    data_from_db = setup_test_database.query(SubMenu).filter(SubMenu.id == UUID(data['id'])).first()
    assert data_from_db.id == UUID(data['id'])
    assert data_from_db.title == new_data['title']
    assert data_from_db.description == new_data['description']


def test_read_submenu_by_id(setup_test_database) -> None:
    response = client.get(reverse('read_submenu_by_id').format(
        target_menu_id=menu_data['id'],
        target_submenu_id=submenu_data['id']
    ))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == submenu_data['id']
    assert data['title'] == submenu_data['title']
    assert data['description'] == submenu_data['description']


def test_read_submenu_by_id_not_found() -> None:
    response = client.get(reverse('read_submenu_by_id').format(
        target_menu_id=menu_data['id'],
        target_submenu_id=submenu_data['id']
    ))
    assert response.status_code == 404
    assert response.json()
    assert response.json()['detail'] == 'submenu not found'


def test_read_submenus(setup_test_database) -> None:
    response = client.get(reverse('read_submenus').format(target_menu_id=menu_data['id']))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data != []
    assert UUID(data[0]['id']) == submenu_data['id']
    assert data[0]['title'] == submenu_data['title']
    assert data[0]['description'] == submenu_data['description']


def test_read_submenus_empty() -> None:
    response = client.get(reverse('read_submenus').format(target_menu_id=menu_data['id']))
    assert response.status_code == 200
    assert response.json() == []


def test_update_submenu(setup_test_database, updated_data: dict[str, str] = updated_submenu_data) -> None:
    response = client.patch(
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

    data_from_db = setup_test_database.query(SubMenu).filter(SubMenu.id == submenu_data['id']).first()
    setup_test_database.refresh(data_from_db)
    assert data_from_db.id == submenu_data['id']
    assert data_from_db.title == updated_data['title']
    assert data_from_db.description == updated_data['description']


def test_delete_submenu(setup_test_database) -> None:
    assert setup_test_database.query(SubMenu).filter(SubMenu.id == submenu_data['id']).first() is not None

    response = client.delete(reverse('update_submenu').format(
        target_menu_id=menu_data['id'],
        target_submenu_id=submenu_data['id']
    ))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == submenu_data['id']
    assert data['title'] == submenu_data['title']
    assert data['description'] == submenu_data['description']

    assert setup_test_database.query(SubMenu).filter(SubMenu.id == submenu_data['id']).first() is None
