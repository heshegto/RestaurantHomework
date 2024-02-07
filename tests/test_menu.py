from uuid import UUID

from app.db.models import Menu

from .conftest import client
from .data import menu_data, new_menu_data, updated_menu_data
from .reverse import reverse


def test_create_menu(setup_test_database, new_data=new_menu_data) -> None:
    response = client.post(reverse('create_menu'), json=new_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert type(UUID(data['id'])) == UUID
    assert data['title'] == new_data['title']
    assert data['description'] == new_data['description']

    data_from_db = setup_test_database.query(Menu).filter(Menu.id == UUID(data['id'])).first()
    assert data_from_db.id == UUID(data['id'])
    assert data_from_db.title == new_data['title']
    assert data_from_db.description == new_data['description']


def test_read_menu_by_id(setup_test_database) -> None:
    response = client.get(reverse('read_menu_by_id').format(target_menu_id=menu_data['id']))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == menu_data['id']
    assert data['title'] == menu_data['title']
    assert data['description'] == menu_data['description']


def test_read_menu_by_id_not_found() -> None:
    response = client.get(reverse('read_menu_by_id').format(target_menu_id=menu_data['id']))
    assert response.status_code == 404
    assert response.json()
    assert response.json()['detail'] == 'menu not found'


def test_read_menus(setup_test_database) -> None:
    response = client.get(reverse('read_menus'))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data != []
    assert UUID(data[0]['id']) == menu_data['id']
    assert data[0]['title'] == menu_data['title']
    assert data[0]['description'] == menu_data['description']


def test_read_menus_empty():
    response = client.get(reverse('read_menus'))
    assert response.status_code == 200
    assert response.json() == []


def test_update_menu(setup_test_database, updated_data=updated_menu_data) -> None:
    response = client.patch(reverse('update_menu').format(target_menu_id=menu_data['id']), json=updated_data)
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == menu_data['id']
    assert data['title'] == updated_data['title']
    assert data['description'] == updated_data['description']

    data_from_db = setup_test_database.query(Menu).filter(Menu.id == menu_data['id']).first()
    setup_test_database.refresh(data_from_db)
    assert data_from_db.id == menu_data['id']
    assert data_from_db.title == updated_data['title']
    assert data_from_db.description == updated_data['description']


def test_delete_menu(setup_test_database) -> None:
    assert setup_test_database.query(Menu).filter(Menu.id == menu_data['id']).first() is not None

    response = client.delete(reverse('delete_menu').format(target_menu_id=menu_data['id']))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == menu_data['id']
    assert data['title'] == menu_data['title']
    assert data['description'] == menu_data['description']

    assert setup_test_database.query(Menu).filter(Menu.id == menu_data['id']).first() is None
