from redis import Redis
from sqlalchemy.orm import Session
from app.db.crud import crud_for_menu as crud
from app.db import cache_database
from uuid import UUID
from app.business import schemas


def get_all_menus(db: Session, cache: Redis):
    keyword = 'menus'
    data = cache_database.read_cache(keyword, cache)
    if data:
        return data
    items = crud.get_menus(db).all()
    cache_database.create_cache(keyword, items, cache)
    return items


def get_one_menu(menu_id: UUID, db: Session, cache: Redis):
    keyword = f'menu:{str(menu_id)}'
    data = cache_database.read_cache(keyword, cache)
    if data:
        return data
    items = crud.get_menu_by_id(db, menu_id)
    cache_database.create_cache(keyword, items, cache)
    return items


def create_menu(menu: schemas.MenuCreate, db: Session, cache: Redis):
    keyword = 'menus'
    cache_database.delete_cache(keyword, cache)
    return crud.create_menu(db, menu)


def update_menu(menu_id: UUID, menu: schemas.MenuCreate, db: Session, cache: Redis):
    keyword = 'menus'
    cache_database.delete_cache(keyword, cache)

    keyword = f'menu:{str(menu_id)}'
    cache_database.delete_cache(keyword, cache)
    return crud.patch_menu(db, menu_id, menu)


def delete_menu(menu_id: UUID, db: Session, cache: Redis):
    keyword = 'menus'
    cache_database.delete_cache(keyword, cache)

    keyword = f'menu:{str(menu_id)}'
    cache_database.delete_cache(keyword, cache)

    keyword = f'menu:{str(menu_id)}:*'
    cache_database.delete_kids_cache(keyword, cache)
    return crud.delete_menu(db, menu_id)
