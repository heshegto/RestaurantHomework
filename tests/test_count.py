from uuid import UUID

from .conftest import client

menu_id: UUID
submenu_id: UUID
dish_id_1: UUID
dish_id_2: UUID


def test_add_menu():
    global menu_id
    new_data = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response = client.post('/api/v1/menus', json=new_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert 'id' in data
    menu_id = data['id']
    assert data['id'] == menu_id


def test_add_submenu():
    global submenu_id
    new_submenu_data = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=new_submenu_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert 'id' in data
    submenu_id = data['id']
    assert data['id'] == submenu_id


def test_add_dish_1():
    global dish_id_1
    new_dish_data = {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=new_dish_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert 'id' in data
    dish_id_1 = data['id']
    assert data['id'] == dish_id_1


def test_add_dish_2():
    global dish_id_2
    new_dish_data = {
        'title': 'My dish 2',
        'description': 'My dish description 2',
        'price': '13.50'
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=new_dish_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert 'id' in data
    dish_id_2 = data['id']
    assert data['id'] == dish_id_2


def test_show_menu():
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data['id'] == menu_id
    assert data['submenus_count'] == 1
    assert data['dishes_count'] == 2


def test_show_submenu():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data['id'] == submenu_id
    assert data['dishes_count'] == 2


def test_drop_submenu():
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200


def test_show_submenus():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert response.json() == []


def test_show_dishes():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    assert response.status_code == 200
    assert response.json() == []


def test_show_menu_2():
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data['id'] == menu_id
    assert data['submenus_count'] == 0
    assert data['dishes_count'] == 0


def test_drop_menu():
    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200


def test_show_menus():
    response = client.get('/api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []
