from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sqlalchemy.orm import Session

from ...db.cache_database import get_redis
from ...db.database import get_db
from ...db.db_loaders.db_loader_for_menu import MenuLoader
from ..schemas import Menu, MenuCreate, MenuRead

router = APIRouter(prefix='/api/v1/menus', tags=['Menu'])
db_loader = MenuLoader()


@router.get('', response_model=list[MenuRead], summary='Get list of all menus')
def read_menus(
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> list[MenuRead]:
    return db_loader.get_all_menus(db, cache)


@router.get('/{target_menu_id}', response_model=MenuRead, summary='Get a menu by it\'s id')
def read_menu_by_id(
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> MenuRead:
    db_menu = db_loader.get_one_menu(target_menu_id, db, cache)
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    return db_menu


@router.post('', response_model=Menu, status_code=201, summary='Create a new menu')
def create_menu(
        menu: MenuCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Menu:
    return db_loader.create_menu(menu, db, cache)


@router.patch('/{target_menu_id}', response_model=Menu, summary='Update a menu')
def update_menu(
        target_menu_id: UUID,
        menu: MenuCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Menu:
    return db_loader.update_menu(target_menu_id, menu, db, cache)


@router.delete('/{target_menu_id}', response_model=Menu, summary='Delete a menu')
def delete_menu(
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Menu:
    return db_loader.delete_menu(target_menu_id, db, cache)
