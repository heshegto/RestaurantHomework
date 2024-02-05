from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from app.db.database import get_db
from app.db.db_loaders import db_loader_for_dish as db_loader

from uuid import UUID
from fastapi import APIRouter
from redis import Redis
from app.db.cache_database import get_redis
router = APIRouter()


@router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', response_model=list[schemas.Dish])
def read_dishes(target_submenu_id: UUID, target_menu_id: UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_redis)):
    return db_loader.get_all_dishes(target_submenu_id, target_menu_id, db, cache)


@router.get(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
    response_model=schemas.Dish
)
def read_dish_by_id(target_dish_id: UUID, target_submenu_id: UUID, target_menu_id: UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_redis)):
    db_dish = db_loader.get_one_dish(target_dish_id, target_submenu_id, target_menu_id, db, cache)
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
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
):
    return db_loader.create_dish(target_submenu_id, target_menu_id, dish, db, cache)


@router.patch(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
    response_model=schemas.Dish
)
def update_dish(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        dish: schemas.DishCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
):
    return db_loader.update_dish(target_dish_id, target_submenu_id, target_menu_id, dish, db, cache)


@router.delete(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
    response_model=schemas.Dish
)
def delete_dish(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
):
    return db_loader.delete_dish(target_dish_id, target_submenu_id, target_menu_id, db, cache)
