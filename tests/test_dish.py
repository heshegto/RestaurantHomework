from uuid import UUID

from app.db.models import Dish

from .conftest import FieldType, client, reverse
from .data import dish_data, menu_data, new_dish_data, submenu_data, updated_dish_data


def test_create_dish(setup_test_database, new_data=new_dish_data):
    response = client.post(reverse(FieldType.DISH, menu_data['id'], submenu_data['id']), json=new_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert type(UUID(data['id'])) == UUID
    assert data['title'] == new_data['title']
    assert data['description'] == new_data['description']

    data_from_db = setup_test_database.query(Dish).filter(Dish.id == UUID(data['id'])).first()
    assert data_from_db.id == UUID(data['id'])
    assert data_from_db.title == new_data['title']
    assert data_from_db.description == new_data['description']


def test_read_dish_by_id(setup_test_database):
    response = client.get(reverse(FieldType.DISH, menu_data['id'], submenu_data['id'], dish_data['id']))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == dish_data['id']
    assert data['title'] == dish_data['title']
    assert data['description'] == dish_data['description']


def test_read_dish_by_id_not_found():
    response = client.get(reverse(FieldType.DISH, menu_data['id'], submenu_data['id'], dish_data['id']))
    assert response.status_code == 404
    assert response.json()
    assert response.json()['detail'] == 'dish not found'


def test_read_dishes(setup_test_database):
    response = client.get(reverse(FieldType.DISH, menu_data['id'], submenu_data['id']))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data != []
    assert UUID(data[0]['id']) == dish_data['id']
    assert data[0]['title'] == dish_data['title']
    assert data[0]['description'] == dish_data['description']


def test_read_dish_empty():
    response = client.get(reverse(FieldType.DISH, menu_data['id'], submenu_data['id']))
    assert response.status_code == 200
    assert response.json() == []


def test_update_dish(setup_test_database, updated_data=updated_dish_data):
    response = client.patch(
        reverse(FieldType.DISH, menu_data['id'], submenu_data['id'], dish_data['id']),
        json=updated_data
    )
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == dish_data['id']
    assert data['title'] == updated_data['title']
    assert data['description'] == updated_data['description']

    data_from_db = setup_test_database.query(Dish).filter(Dish.id == dish_data['id']).first()
    setup_test_database.refresh(data_from_db)
    assert data_from_db.id == dish_data['id']
    assert data_from_db.title == updated_data['title']
    assert data_from_db.description == updated_data['description']


def test_delete_dish(setup_test_database):
    assert setup_test_database.query(Dish).filter(Dish.id == dish_data['id']).first() is not None

    response = client.delete(reverse(FieldType.DISH, menu_data['id'], submenu_data['id'], dish_data['id']))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data['id']) == dish_data['id']
    assert data['title'] == dish_data['title']
    assert data['description'] == dish_data['description']

    assert setup_test_database.query(Dish).filter(Dish.id == dish_data['id']).first() is None
