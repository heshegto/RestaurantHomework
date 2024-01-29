from .conftest import client
from uuid import UUID


menu_id: UUID
submenu_id: UUID
dish_id: UUID


def test_create_dish():
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
    submenu_id = response.json()["id"]

    global dish_id
    new_dish_data = {
        "title": "My submenu",
        "description": "My submenu description",
        "price": "3.20"
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=new_dish_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert "id" in data
    dish_id = data["id"]

    assert data["title"] == new_dish_data["title"]
    assert data["description"] == new_dish_data["description"]
    assert data["price"] == new_dish_data["price"]


def test_read_dish():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert "id" in data
    assert "title" in data
    assert "description" in data
    assert "price" in data


def test_read_dishes():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data != []
    assert "id" in data[0]
    assert "title" in data[0]
    assert "description" in data[0]
    assert "price" in data[0]


def test_update_dish():
    updated_data = {
        "title": "My updated submenu",
        "description": "My updated submenu description",
        "price": "8.8"
    }
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json=updated_data)
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert "id" in data
    assert data["id"] == dish_id

    assert data["title"] == updated_data["title"]
    assert data["description"] == updated_data["description"]
    assert data["price"] == updated_data["price"] + '0'


def test_delete_submenu():
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert "id" in data
    assert data["id"] == dish_id
