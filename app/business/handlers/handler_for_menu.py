from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sqlalchemy.orm import Session

from ...db.cache_database import get_redis
from ...db.crud import MenuCRUD
from ...db.database import get_db
from ...db.db_loaders.db_loader_base import BaseLoader
from ..schemas import Menu, MenuCreate, MenuRead
from .help_funcs import all_responses, is_menu_none

router = APIRouter(prefix='/api/v1/menus', tags=['Menu'])
db_loader = BaseLoader(MenuCRUD())


@router.get('', response_model=list[MenuRead], summary='Get list of all menus')
def read_menus(
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> list[MenuRead] | list[dict[str, str | int]]:
    return db_loader.get_all(db, cache)


@router.get(
    '/{target_menu_id}',
    response_model=MenuRead,
    summary='Get a menu by it\'s id',
    responses={404: all_responses['menu'][404]}
)
def read_menu_by_id(
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> MenuRead | list[dict[str, str | int]]:
    return is_menu_none(db_loader.get_one(db, cache, target_menu_id))


@router.post(
    '',
    response_model=Menu,
    status_code=201,
    summary='Create a new menu',
    responses={401: all_responses['menu'][401]}
)
def create_menu(
        menu: MenuCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Menu:
    db_menu = db_loader.create(db, cache, menu)
    if db_menu is None:
        raise HTTPException(
            status_code=401,
            detail='Menu creation error'
        )
    return db_menu


@router.patch(
    '/{target_menu_id}',
    response_model=Menu,
    summary='Update a menu',
    responses={404: all_responses['menu'][404]}
)
def update_menu(
        target_menu_id: UUID,
        menu: MenuCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Menu | list[dict[str, str | int]]:
    return is_menu_none(db_loader.update(db, cache, menu, target_menu_id))


@router.delete(
    '/{target_menu_id}',
    response_model=Menu,
    summary='Delete a menu',
    responses={404: all_responses['menu'][404]}
)
def delete_menu(
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Menu | list[dict[str, str | int]]:
    return is_menu_none(db_loader.delete(db, cache, target_menu_id))
