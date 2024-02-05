from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sqlalchemy.orm import Session

from ...db.cache_database import get_redis
from ...db.database import get_db
from ...db.db_loaders.db_loader_for_dish import DishLoader
from ..schemas import Dish, DishCreate

router = APIRouter(prefix='/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', tags=['Dish'])
db_loader = DishLoader()


@router.get('', response_model=list[Dish], summary='Get list of dishes for a given submenu')
def read_dishes(
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> list[Dish]:
    return db_loader.get_all_dishes(target_submenu_id, target_menu_id, db, cache)


@router.get('/{target_dish_id}', response_model=Dish, summary='Get a dish by it\'s id')
def read_dish_by_id(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Dish:
    db_dish = db_loader.get_one_dish(target_dish_id, target_submenu_id, target_menu_id, db, cache)
    if db_dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    return db_dish


@router.post('', response_model=Dish, status_code=201, summary='Create a new dish for a given submenu')
def create_dish(
        target_submenu_id: UUID,
        target_menu_id: UUID,
        dish: DishCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Dish:
    return db_loader.create_dish(target_submenu_id, target_menu_id, dish, db, cache)


@router.patch('/{target_dish_id}', response_model=Dish, summary='Update a dish')
def update_dish(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        dish: DishCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Dish:
    return db_loader.update_dish(target_dish_id, target_submenu_id, target_menu_id, dish, db, cache)


@router.delete('/{target_dish_id}', response_model=Dish, summary='Delete a dish')
def delete_dish(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Dish:
    return db_loader.delete_dish(target_dish_id, target_submenu_id, target_menu_id, db, cache)
