from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import crud
from .. import schemas
from app.db.database import get_db

from uuid import UUID
from fastapi import APIRouter
router = APIRouter()

@router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', response_model=list[schemas.Dish])
def read_dishes(target_submenu_id: UUID, db: Session = Depends(get_db)):
    return crud.get_dishes(db, target_submenu_id)


@router.get(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
    response_model=schemas.Dish
)
def read_dish_by_id(target_dish_id: UUID, target_submenu_id: UUID, db: Session = Depends(get_db)):
    db_dish = crud.get_dish_by_id(db, target_dish_id, target_submenu_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish


@router.post(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
    response_model=schemas.Dish,
    status_code=201
)
def create_dish(
        target_submenu_id: UUID,
        target_menu_id: UUID,
        dish: schemas.DishCreate,
        db: Session = Depends(get_db)
):
    return crud.create_dish(db, target_submenu_id, target_menu_id, dish)


@router.patch(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
    response_model=schemas.Dish
)
def update_dish(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        dish: schemas.DishCreate,
        db: Session = Depends(get_db)
):
    return crud.patch_dish(db, target_dish_id, target_submenu_id, dish)


@router.delete(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
    response_model=schemas.Dish
)
def delete_dish(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: Session = Depends(get_db)
):
    return crud.delete_dish(db, target_dish_id, target_submenu_id, target_menu_id)
