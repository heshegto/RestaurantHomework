from .conftest import client
from uuid import UUID


menu_id: UUID


def test_create_menu():
    global menu_id
    new_data = {
        "title": "My menu",
        "description": "My menu description"
    }
    response = client.post("/api/v1/menus", json=new_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert "id" in data
    menu_id = data["id"]

    assert data["title"] == new_data["title"]
    assert data["description"] == new_data["description"]


def test_read_menu():
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert "id" in data
    assert "title" in data
    assert "description" in data


def test_read_menus():
    response = client.get("/api/v1/menus")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data != []
    assert "id" in data[0]
    assert "title" in data[0]
    assert "description" in data[0]


def test_update_menu():
    updated_data = {
        "title": "My updated menu",
        "description": "My updated menu description"
    }
    response = client.patch(f"/api/v1/menus/{menu_id}", json=updated_data)
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert "id" in data
    assert data["id"] == menu_id

    assert data["title"] == updated_data["title"]
    assert data["description"] == updated_data["description"]


def test_delete_menu():
    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert "id" in data
    assert data["id"] == menu_id
