from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import crud
from .. import schemas
from app.db.database import get_db

from uuid import UUID
from fastapi import APIRouter
router = APIRouter()


@router.get('/api/v1/menus/{target_menu_id}/submenus', response_model=list[schemas.SubMenuRead])
def read_submenus(target_menu_id: UUID, db: Session = Depends(get_db)):
    return crud.get_submenus(db, target_menu_id)


@router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.SubMenuRead)
def read_submenu_by_id(target_submenu_id: UUID, target_menu_id: UUID, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu_by_id(db, target_submenu_id, target_menu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu


@router.post('/api/v1/menus/{target_menu_id}/submenus', response_model=schemas.SubMenu, status_code=201)
def create_submenu(target_menu_id: UUID, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)):
    return crud.create_submenu(db, target_menu_id, submenu)


@router.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.SubMenu)
def update_submenu(target_submenu_id: UUID, target_menu_id: UUID, submenu: schemas.SubMenuCreate,
                   db: Session = Depends(get_db)):
    return crud.patch_submenu(db, target_submenu_id, target_menu_id, submenu)


@router.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.SubMenu)
def delete_submenu(target_submenu_id: UUID, target_menu_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_submenu(db, target_submenu_id, target_menu_id)
