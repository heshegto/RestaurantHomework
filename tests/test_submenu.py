from .conftest import client
from uuid import UUID


menu_id: UUID
submenu_id: UUID


def test_create_submenu():
    global menu_id
    new_menu_data = {
        "title": "My menu",
        "description": "My menu description"
    }
    response = client.post("/api/v1/menus", json=new_menu_data)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    global submenu_id
    new_submenu_data = {
        "title": "My submenu",
        "description": "My submenu description"
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=new_submenu_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert "id" in data
    submenu_id = data["id"]

    assert data["title"] == new_submenu_data["title"]
    assert data["description"] == new_submenu_data["description"]


def test_read_submenu():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert "id" in data
    assert "title" in data
    assert "description" in data


def test_read_submenus():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data != []
    assert "id" in data[0]
    assert "title" in data[0]
    assert "description" in data[0]


def test_update_submenu():
    updated_data = {
        "title": "My updated submenu",
        "description": "My updated submenu description"
    }
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}", json=updated_data)
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert "id" in data
    assert data["id"] == submenu_id

    assert data["title"] == updated_data["title"]
    assert data["description"] == updated_data["description"]


def test_delete_submenu():
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert "id" in data
    assert data["id"] == submenu_id
