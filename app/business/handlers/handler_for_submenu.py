from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sqlalchemy.orm import Session

from ...db.cache_database import get_redis
from ...db.crud import SubMenuCRUD
from ...db.database import get_db
from ...db.db_loaders.db_loader_base import BaseLoader
from ..schemas import SubMenu, SubMenuCreate, SubMenuRead
from .help_funcs import all_responses, is_submenu_none

router = APIRouter(prefix='/api/v1/menus/{target_menu_id}/submenus', tags=['Submenu'])
db_loader = BaseLoader(SubMenuCRUD())


@router.get('', response_model=list[SubMenuRead], summary='Get list of submenus for a given menu')
def read_submenus(
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> list[SubMenuRead] | list[dict[str, int]]:
    return db_loader.get_all(db, cache, target_menu_id)


@router.get(
    '/{target_submenu_id}',
    response_model=SubMenuRead,
    summary='Get a submenu by it\'s id',
    responses={404: all_responses['submenu'][404]}
)
def read_submenu_by_id(
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> SubMenuRead | list[dict[str, int]]:
    return is_submenu_none(db_loader.get_one(db, cache, target_submenu_id, target_menu_id))


@router.post(
    '',
    response_model=SubMenu,
    status_code=201,
    summary='Create a new submenu for given menu',
    responses={401: all_responses['submenu'][401]}
)
def create_submenu(
        target_menu_id: UUID,
        submenu: SubMenuCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> SubMenu:
    db_submenu = db_loader.create(db, cache, submenu, target_menu_id)
    if db_submenu is None:
        raise HTTPException(
            status_code=401,
            detail='SubMenu creation error'
        )
    return db_submenu


@router.patch(
    '/{target_submenu_id}',
    response_model=SubMenu,
    summary='Update a submenu',
    responses={404: all_responses['submenu'][404]}
)
def update_submenu(
        target_submenu_id: UUID,
        target_menu_id: UUID,
        submenu: SubMenuCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> SubMenu | list[dict[str, int]]:
    return is_submenu_none(db_loader.update(db, cache, submenu, target_submenu_id, target_menu_id))


@router.delete(
    '/{target_submenu_id}',
    response_model=SubMenu,
    summary='Delete a submenu',
    responses={404: all_responses['submenu'][404]}
)
def delete_submenu(
        target_submenu_id: UUID,
        target_menu_id: UUID, db:
        Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> SubMenu | list[dict[str, int]]:
    return is_submenu_none(db_loader.delete(db, cache, target_submenu_id, target_menu_id))
