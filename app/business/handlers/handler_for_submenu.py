from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sqlalchemy.orm import Session

from app.db.cache_database import get_redis
from app.db.database import get_db
from app.db.db_loaders import db_loader_for_submenu as db_loader

from .. import schemas

router = APIRouter()


@router.get('/api/v1/menus/{target_menu_id}/submenus', response_model=list[schemas.SubMenuRead], tags=['Submenu'], summary='Get list of submenus for a given menu')
def read_submenus(target_menu_id: UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_redis)):
    return db_loader.get_all_submenus(target_menu_id, db, cache)


@router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.SubMenuRead, tags=['Submenu'], summary='Get a submenu by it\'s id')
def read_submenu_by_id(target_submenu_id: UUID, target_menu_id: UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_redis)):
    db_submenu = db_loader.get_one_submenu(target_submenu_id, target_menu_id, db, cache)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    return db_submenu


@router.post('/api/v1/menus/{target_menu_id}/submenus', response_model=schemas.SubMenu, status_code=201, tags=['Submenu'], summary='Create a new submenu for given menu')
def create_submenu(target_menu_id: UUID, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db), cache: Redis = Depends(get_redis)):
    return db_loader.create_submenu(target_menu_id, submenu, db, cache)


@router.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.SubMenu, tags=['Submenu'], summary='Update a submenu')
def update_submenu(target_submenu_id: UUID, target_menu_id: UUID, submenu: schemas.SubMenuCreate,
                   db: Session = Depends(get_db),
                   cache: Redis = Depends(get_redis)):
    return db_loader.update_submenu(target_submenu_id, target_menu_id, submenu, db, cache)


@router.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.SubMenu, tags=['Submenu'], summary='Delete a submenu')
def delete_submenu(target_submenu_id: UUID, target_menu_id: UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_redis)):
    return db_loader.delete_submenu(target_submenu_id, target_menu_id, db, cache)
