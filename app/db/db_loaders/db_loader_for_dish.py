from redis import Redis
from sqlalchemy.orm import Session
from app.db.crud import crud_for_dish as crud
from app.db import cache_database
from uuid import UUID
from app.business import schemas


def get_all_dishes(submenu_id: UUID, menu_id: UUID, db: Session, cache: Redis):
    keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dishes'
    data = cache_database.read_cache(keyword, cache)
    if data:
        return data
    items = crud.get_dishes(db, submenu_id).all()
    cache_database.create_cache(keyword, items, cache)
    return items


def get_one_dish(dish_id: UUID, submenu_id: UUID, menu_id: UUID, db: Session, cache: Redis):
    keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dish:{str(dish_id)}'
    data = cache_database.read_cache(keyword, cache)
    if data:
        return data
    items = crud.get_dish_by_id(db, dish_id, submenu_id)
    cache_database.create_cache(keyword, items, cache)
    return items


def create_dish(submenu_id: UUID, menu_id: UUID, dish: schemas.DishCreate, db: Session, cache: Redis):
    keyword = 'menus'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenus'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenu:{submenu_id}'
    cache_database.delete_cache(keyword, cache)
    return crud.create_dish(db, submenu_id, dish)


def update_dish(dish_id: UUID, submenu_id: UUID, menu_id: UUID, dish: schemas.DishCreate, db: Session, cache: Redis):
    keyword = 'menus'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenus'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dishes'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dish:{str(dish_id)}'
    cache_database.delete_cache(keyword, cache)
    return crud.patch_dish(db, dish_id, submenu_id, dish)


def delete_dish(dish_id: UUID, submenu_id: UUID, menu_id: UUID, db: Session, cache: Redis):
    keyword = 'menus'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenus'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dishes'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dish:{str(dish_id)}'
    cache_database.delete_cache(keyword, cache)
    return crud.delete_dish(db, dish_id, submenu_id)
