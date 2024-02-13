import os
import openpyxl
import requests

file_path = '../admin/Menu.xlsx'
last_date = 0


def get_last_modified_date(file_path):
    try:
        return os.stat(file_path).st_mtime
    except FileNotFoundError:
        print("File Not Found")
    except Exception as e:
        print("Error happened:", e)


def check_for_updates():
    global last_date
    if os.path.exists(file_path):
        last_modified_date = get_last_modified_date(file_path)
        if last_modified_date != last_date:
            last_date = last_modified_date
            return last_date
        else:
            return False
    else:
        raise Exception('File for synchronization does not exist')


def get_base_from_file():
    base_from_file = []
    workbook = openpyxl.load_workbook(file_path)
    try:
        sheet = workbook.active
    finally:
        workbook.close()

    for row in sheet.iter_rows(values_only=True):
        item = {}
        if type(row[0]) is int:
            item['title'] = row[1]
            item['description'] = row[2]
            item['submenus'] = []

            base_from_file.append(item)
        elif type(row[1]) is int:
            item['title'] = row[2]
            item['description'] = row[3]
            item['dishes'] = []
            base_from_file[-1]['submenus'].append(item)
        elif type(row[2]) is int:
            item['title'] = row[3]
            item['description'] = row[4]
            item['price'] = row[5]
            base_from_file[-1]['submenus'][-1]['dishes'].append(item)
    return base_from_file


def get_list_of_titles_and_ids(item_list: list[dict]) -> dict:
    result = {}
    for item_ in item_list:
        result[item_['title']] = item_['id']
    return result


def creat_dishes(submenu: dict, menu_id: str, submenu_id: str) -> None:
    url = f'http://127.0.0.1:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'
    for dish in submenu['dishes']:
        requests.post(url, json={'title': dish['title'], 'description': dish['description'],
                                 'price': f'{round(float(dish['price']), 2):.2f}'})


def creat_submenus(menu: dict, menu_id: str) -> None:
    url = f'http://127.0.0.1:8000/api/v1/menus/{menu_id}/submenus'
    for submenu in menu['submenus']:
        submenu_id = requests.post(url, json={'title': submenu['title'], 'description': submenu['description']}).json()[
            'id']
        creat_dishes(submenu, menu_id, submenu_id)


def push_new() -> None:
    url = 'http://127.0.0.1:8000/api/v1/menus'
    menus_from_base = requests.get(url).json()
    for menu_item in get_base_from_file():
        if menu_item['title'] not in get_list_of_titles_and_ids(menus_from_base):
            menu_id = \
            requests.post(url, json={'title': menu_item['title'], 'description': menu_item['description']}).json()['id']
            creat_submenus(menu_item, menu_id)
        else:
            for submenu_item in menu_item['submenus']:
                menu_id = get_list_of_titles_and_ids(menus_from_base)[menu_item['title']]
                suburl = f'http://127.0.0.1:8000/api/v1/menus/{menu_id}/submenus'
                submenus_from_base = requests.get(suburl).json()
                if submenu_item['title'] not in get_list_of_titles_and_ids(submenus_from_base):
                    submenu_id = requests.post(suburl, json={'title': submenu_item['title'],
                                                             'description': submenu_item['description']}).json()['id']
                    creat_dishes(submenu_item, menu_id, submenu_id)
                else:
                    for dish_item in submenu_item['dishes']:
                        submenu_id = get_list_of_titles_and_ids(submenus_from_base)[submenu_item['title']]
                        dishurl = f'http://127.0.0.1:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'
                        dishes_from_base = requests.get(suburl).json()
                        if dish_item['title'] not in get_list_of_titles_and_ids(dishes_from_base):
                            requests.post(dishurl,
                                          json={'title': dish_item['title'], 'description': dish_item['description'],
                                                'price': f'{round(float(dish_item['price']), 2):.2f}'})


def find_submenus_in_menu(target_menus: list[dict], title: str) -> list:
    for dictionary in target_menus:
        if title == dictionary['title']:
            return dictionary['submenus']
    return []


def find_dishes_in_submenu(target_submenus: list[dict], title: str) -> list:
    for dictionary in target_submenus:
        if title == dictionary['title']:
            return dictionary['dishes']
    return []


def get_list_of_titles(item_list: list) -> list:
    titles = []
    for item_ in item_list:
        titles.append(item_['title'])
    return titles


def del_old() -> None:
    url = 'http://127.0.0.1:8000/api/v1/menus'
    menus_from_base = requests.get(url).json()
    menu_list_from_file = get_list_of_titles(get_base_from_file())
    for menu in menus_from_base:
        if menu['title'] not in menu_list_from_file:
            menurl = url + '/' + menu['id']
            requests.delete(menurl)
        else:
            url2 = f'http://127.0.0.1:8000/api/v1/menus/{menu["id"]}/submenus'
            submenus_from_base = requests.get(url2).json()
            submenu_list_from_file = get_list_of_titles(find_submenus_in_menu(get_base_from_file(), menu['title']))
            for submenu in submenus_from_base:
                if submenu['title'] not in submenu_list_from_file:
                    suburl = url + '/' + submenu['id']
                    requests.delete(suburl)
                else:
                    url3 = f'http://127.0.0.1:8000/api/v1/menus/{menu["id"]}/submenus/{submenu["id"]}/dishes'
                    dish_from_base = requests.get(url3).json()
                    dish_list_from_file = get_list_of_titles(
                        find_dishes_in_submenu(find_submenus_in_menu(get_base_from_file(), menu['title']),
                                               submenu['title']))
                    for dish in dish_from_base:
                        if dish['title'] not in dish_list_from_file:
                            dishurl = url3 + '/' + dish['id']
                            requests.delete(dishurl)
