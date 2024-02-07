from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sqlalchemy.orm import Session

from ...db.cache_database import get_redis
from ...db.crud import DishCRUD
from ...db.database import get_db
from ...db.db_loaders.db_loader_base import BaseLoader
from ..schemas import Dish, DishCreate
from .help_funcs import all_responses, is_dish_none

router = APIRouter(prefix='/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', tags=['Dish'])
db_loader = BaseLoader(DishCRUD())


@router.get('', response_model=list[Dish], summary='Get list of dishes for a given submenu')
def read_dishes(
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> list[Dish] | list[dict[str, str | int]]:
    return db_loader.get_all(db, cache, target_submenu_id, target_menu_id)


@router.get(
    '/{target_dish_id}',
    response_model=Dish,
    summary='Get a dish by it\'s id',
    responses={404: all_responses['dish'][404]}
)
def read_dish_by_id(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Dish | list[dict[str, str | int]]:
    return is_dish_none(db_loader.get_one(db, cache, target_dish_id, target_submenu_id, target_menu_id))


@router.post(
    '',
    response_model=Dish,
    status_code=201,
    summary='Create a new dish for a given submenu',
    responses={401: all_responses['dish'][401]}
)
def create_dish(
        target_submenu_id: UUID,
        target_menu_id: UUID,
        dish: DishCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Dish:
    db_dish = db_loader.create(db, cache, dish, target_submenu_id, target_menu_id)
    if db_dish is None:
        raise HTTPException(
            status_code=401,
            detail='Dish creation error'
        )
    return db_dish


@router.patch(
    '/{target_dish_id}',
    response_model=Dish,
    summary='Update a dish',
    responses={404: all_responses['dish'][404]}
)
def update_dish(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        dish: DishCreate,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Dish | list[dict[str, str | int]]:
    return is_dish_none(db_loader.update(db, cache, dish, target_dish_id, target_submenu_id, target_menu_id))


@router.delete(
    '/{target_dish_id}',
    response_model=Dish,
    summary='Delete a dish',
    responses={404: all_responses['dish'][404]}
)
def delete_dish(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Dish | list[dict[str, str | int]]:
    return is_dish_none(db_loader.delete(db, cache, target_dish_id, target_submenu_id, target_menu_id))
