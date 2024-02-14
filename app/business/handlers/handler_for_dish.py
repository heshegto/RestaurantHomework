from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.cache import cache_invalidation
from app.databases.cache.cache import get_redis
from app.databases.db.crud import DishCRUD
from app.databases.db.database import get_db
from app.databases.db_cache_switch import DBOrCache

from ..schemas import Dish, DishCreate
from .services import all_responses, is_dish_none

router = APIRouter(prefix='/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', tags=['Dish'])
db_loader = DBOrCache(DishCRUD())


@router.get('', response_model=list[Dish], summary='Get list of dishes for a given submenu')
async def read_dishes(
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> list[Dish] | list[dict[str, str | int]]:
    return await db_loader.get_all(db, cache, target_submenu_id, target_menu_id)


@router.get(
    '/{target_dish_id}',
    response_model=Dish,
    summary='Get a dish by it\'s id',
    responses={404: all_responses['dish'][404]}
)
async def read_dish_by_id(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Dish | list[dict[str, str | int]]:
    return is_dish_none(await db_loader.get_one(db, cache, target_dish_id, target_submenu_id, target_menu_id))


@router.post(
    '',
    response_model=Dish,
    status_code=201,
    summary='Create a new dish for a given submenu',
    responses={401: all_responses['dish'][401]}
)
async def create_dish(
        background_tasks: BackgroundTasks,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        dish: DishCreate,
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Dish:
    background_tasks.add_task(
        cache_invalidation.invalidation_on_creation,
        cache, target_submenu_id, target_menu_id
    )
    db_dish = await db_loader.create(db, dish, target_submenu_id)
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
async def update_dish(
        background_tasks: BackgroundTasks,
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        dish: DishCreate,
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Dish | list[dict[str, str | int]]:
    background_tasks.add_task(
        cache_invalidation.invalidation_on_update,
        cache, target_dish_id, target_submenu_id, target_menu_id
    )
    return is_dish_none(await db_loader.update(db, dish, target_dish_id))


@router.delete(
    '/{target_dish_id}',
    response_model=Dish,
    summary='Delete a dish',
    responses={404: all_responses['dish'][404]}
)
async def delete_dish(
        background_tasks: BackgroundTasks,
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Dish | list[dict[str, str | int]]:
    background_tasks.add_task(
        cache_invalidation.invalidation_on_delete,
        cache, target_dish_id, target_submenu_id, target_menu_id
    )
    return is_dish_none(await db_loader.delete(db, target_dish_id))
