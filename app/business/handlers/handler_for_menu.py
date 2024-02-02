from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import crud
from .. import schemas
from app.db.database import get_db

from uuid import UUID
from fastapi import APIRouter
router = APIRouter()


@router.get('/api/v1/menus', response_model=list[schemas.MenuRead])
def read_menus(db: Session = Depends(get_db)):
    return crud.get_menus(db)


@router.get('/api/v1/menus/{target_menu_id}', response_model=schemas.MenuRead)
def read_menu_by_id(target_menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, target_menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu


@router.post('/api/v1/menus', response_model=schemas.Menu, status_code=201)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    return crud.create_menu(db, menu)


@router.patch('/api/v1/menus/{target_menu_id}', response_model=schemas.Menu)
def update_menu(target_menu_id: UUID, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    return crud.patch_menu(db, target_menu_id, menu)


@router.delete('/api/v1/menus/{target_menu_id}', response_model=schemas.Menu)
def delete_menu(target_menu_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_menu(db, target_menu_id)