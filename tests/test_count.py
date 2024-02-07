from uuid import UUID

from .conftest import client
from .reverse import reverse

menu_id: UUID
submenu_id: UUID
dish_id_1: UUID
dish_id_2: UUID


def test_add_menu() -> None:
    global menu_id
    new_data = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response = client.post(reverse('create_menu'), json=new_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert 'id' in data
    menu_id = data['id']
    assert data['id'] == menu_id


def test_add_submenu() -> None:
    global submenu_id
    new_submenu_data = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response = client.post(reverse('create_submenu').format(target_menu_id=menu_id), json=new_submenu_data)
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert 'id' in data
    submenu_id = data['id']
    assert data['id'] == submenu_id


def test_add_dish_1() -> None:
    global dish_id_1
    new_dish_data = {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    }
    response = client.post(
        reverse('create_dish').format(target_menu_id=menu_id, target_submenu_id=submenu_id),
        json=new_dish_data
    )
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert 'id' in data
    dish_id_1 = data['id']
    assert data['id'] == dish_id_1


def test_add_dish_2() -> None:
    global dish_id_2
    new_dish_data = {
        'title': 'My dish 2',
        'description': 'My dish description 2',
        'price': '13.50'
    }
    response = client.post(
        reverse('create_dish').format(target_menu_id=menu_id, target_submenu_id=submenu_id),
        json=new_dish_data
    )
    assert response.status_code == 201

    assert response.json()
    data = response.json()

    assert 'id' in data
    dish_id_2 = data['id']
    assert data['id'] == dish_id_2


def test_show_menu() -> None:
    response = client.get(reverse('read_menu_by_id').format(target_menu_id=menu_id))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data['id'] == menu_id
    assert data['submenus_count'] == 1
    assert data['dishes_count'] == 2


def test_show_submenu() -> None:
    response = client.get(reverse('read_submenu_by_id').format(target_menu_id=menu_id, target_submenu_id=submenu_id))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data['id'] == submenu_id
    assert data['dishes_count'] == 2


def test_drop_submenu() -> None:
    response = client.delete(reverse('delete_submenu').format(target_menu_id=menu_id, target_submenu_id=submenu_id))
    assert response.status_code == 200


def test_show_submenus() -> None:
    response = client.get(reverse('read_submenus').format(target_menu_id=menu_id))
    assert response.status_code == 200
    assert response.json() == []


def test_show_dishes() -> None:
    response = client.get(reverse('read_dishes').format(target_menu_id=menu_id, target_submenu_id=submenu_id))
    assert response.status_code == 200
    assert response.json() == []


def test_show_menu_2() -> None:
    response = client.get(reverse('read_menu_by_id').format(target_menu_id=menu_id))
    assert response.status_code == 200

    assert response.json()
    data = response.json()

    assert data['id'] == menu_id
    assert data['submenus_count'] == 0
    assert data['dishes_count'] == 0


def test_drop_menu() -> None:
    response = client.delete(reverse('delete_menu').format(target_menu_id=menu_id))
    assert response.status_code == 200


def test_show_menus() -> None:
    response = client.get(reverse('read_menus'))
    assert response.status_code == 200
    assert response.json() == []
