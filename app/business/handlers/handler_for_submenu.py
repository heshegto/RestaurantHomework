from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sqlalchemy.orm import Session

from ...db.cache_database import get_redis
from ...db.database import get_db
from ...db.db_loaders.db_loader_for_submenu import SubmenuLoader
from ..schemas import SubMenu, SubMenuCreate, SubMenuRead

router = APIRouter(prefix='/api/v1/menus/{target_menu_id}/submenus', tags=['Submenu'])
db_loader = SubmenuLoader()


@router.get('', response_model=list[SubMenuRead], summary='Get list of submenus for a given menu')
def read_submenus(
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> list[SubMenuRead]:
    return db_loader.get_all_submenus(target_menu_id, db, cache)


@router.get('/{target_submenu_id}', response_model=SubMenuRead, summary='Get a submenu by it\'s id')
def read_submenu_by_id(
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> SubMenuRead:
    db_submenu = db_loader.get_one_submenu(target_submenu_id, target_menu_id, db, cache)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    return db_submenu


@router.post('', response_model=SubMenu, status_code=201, summary='Create a new submenu for given menu')
def create_submenu(
        target_menu_id: UUID,
        submenu: SubMenuCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> SubMenu:
    return db_loader.create_submenu(target_menu_id, submenu, db, cache)


@router.patch('/{target_submenu_id}', response_model=SubMenu, summary='Update a submenu')
def update_submenu(
        target_submenu_id: UUID,
        target_menu_id: UUID,
        submenu: SubMenuCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> SubMenu:
    return db_loader.update_submenu(target_submenu_id, target_menu_id, submenu, db, cache)


@router.delete('/{target_submenu_id}', response_model=SubMenu, summary='Delete a submenu')
def delete_submenu(
        target_submenu_id: UUID,
        target_menu_id: UUID, db:
        Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> SubMenu:
    return db_loader.delete_submenu(target_submenu_id, target_menu_id, db, cache)
