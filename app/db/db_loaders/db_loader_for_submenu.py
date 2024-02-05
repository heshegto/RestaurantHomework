from uuid import UUID

from redis import Redis
from sqlalchemy.orm import Session

from app.business import schemas
from app.db import cache_database
from app.db.crud import crud_for_submenu as crud


def get_all_submenus(menu_id: UUID, db: Session, cache: Redis):
    keyword = f'menu:{str(menu_id)}:submenus'
    data = cache_database.read_cache(keyword, cache)
    if data:
        return data
    items = crud.get_submenus(db, menu_id).all()
    cache_database.create_cache(keyword, items, cache)
    return items


def get_one_submenu(submenu_id: UUID, menu_id: UUID, db: Session, cache: Redis):
    keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}'
    data = cache_database.read_cache(keyword, cache)
    if data:
        return data
    items = crud.get_submenu_by_id(db, submenu_id, menu_id)
    cache_database.create_cache(keyword, items, cache)
    return items


def create_submenu(menu_id: UUID, submenu: schemas.SubMenuCreate, db: Session, cache: Redis):
    keyword = 'menus'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenus'
    cache_database.delete_cache(keyword, cache)
    return crud.create_submenu(db, menu_id, submenu)


def update_submenu(submenu_id: UUID, menu_id: UUID, submenu: schemas.SubMenuCreate, db: Session, cache: Redis):
    keyword = 'menus'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenus'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}'
    cache_database.delete_cache(keyword, cache)
    return crud.patch_submenu(db, submenu_id, menu_id, submenu)


def delete_submenu(submenu_id: UUID, menu_id: UUID, db: Session, cache: Redis):
    keyword = 'menus'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenus'
    cache_database.delete_cache(keyword, cache)
    keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}'
    cache_database.delete_cache(keyword, cache)

    keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:*'
    cache_database.delete_kids_cache(keyword, cache)
    return crud.delete_submenu(db, submenu_id, menu_id)
