from .conftest import client
from uuid import UUID
from .data import menu_data, submenu_data, new_submenu_data, updated_submenu_data
from app.models import SubMenu


def test_create_submenu(setup_test_database, new_data=new_submenu_data):
    response = client.post(f"/api/v1/menus/{menu_data['id']}/submenus", json=new_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert type(UUID(data["id"])) == UUID
    assert data["title"] == new_data["title"]
    assert data["description"] == new_data["description"]

    data_from_db = setup_test_database.query(SubMenu).filter(SubMenu.id == UUID(data["id"])).first()
    assert data_from_db.id == UUID(data["id"])
    assert data_from_db.title == new_data["title"]
    assert data_from_db.description == new_data["description"]


def test_read_submenu_by_id(setup_test_database):
    response = client.get(f"/api/v1/menus/{menu_data['id']}/submenus/{submenu_data['id']}")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data["id"]) == submenu_data["id"]
    assert data["title"] == submenu_data["title"]
    assert data["description"] == submenu_data["description"]


def test_read_submenu_by_id_not_found():
    response = client.get(f"/api/v1/menus/{menu_data['id']}/submenus/{submenu_data['id']}")
    assert response.status_code == 404
    assert response.json()
    assert response.json()['detail'] == "submenu not found"


def test_read_submenus(setup_test_database):
    response = client.get(f"/api/v1/menus/{menu_data['id']}/submenus")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data != []
    assert UUID(data[0]["id"]) == submenu_data["id"]
    assert data[0]["title"] == submenu_data["title"]
    assert data[0]["description"] == submenu_data["description"]


def test_read_submenus_empty():
    response = client.get(f"/api/v1/menus/{menu_data['id']}/submenus")
    assert response.status_code == 200
    assert response.json() == []


def test_update_submenu(setup_test_database, updated_data=updated_submenu_data):
    response = client.patch(f"/api/v1/menus/{menu_data['id']}/submenus/{submenu_data['id']}", json=updated_data)
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data["id"]) == submenu_data['id']
    assert data["title"] == updated_data["title"]
    assert data["description"] == updated_data["description"]

    data_from_db = setup_test_database.query(SubMenu).filter(SubMenu.id == submenu_data['id']).first()
    setup_test_database.refresh(data_from_db)
    assert data_from_db.id == submenu_data['id']
    assert data_from_db.title == updated_data["title"]
    assert data_from_db.description == updated_data["description"]


def test_delete_submenu(setup_test_database):
    assert setup_test_database.query(SubMenu).filter(SubMenu.id == submenu_data['id']).first() is not None

    response = client.delete(f"/api/v1/menus/{menu_data['id']}/submenus/{submenu_data['id']}")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert UUID(data["id"]) == submenu_data['id']
    assert data["title"] == submenu_data["title"]
    assert data["description"] == submenu_data["description"]

    assert setup_test_database.query(SubMenu).filter(SubMenu.id == submenu_data['id']).first() is None
