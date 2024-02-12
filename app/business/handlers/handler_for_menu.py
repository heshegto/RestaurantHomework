from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.cash.cache import get_redis
from app.databases.db.crud import MenuCRUD
from app.databases.db.database import get_db
from app.databases.db_cache_switch import DBOrCache
from ..schemas import Menu, MenuCreate, MenuRead
from .services import all_responses, is_menu_none

router = APIRouter(prefix='/api/v1/menus', tags=['Menu'])
db_loader = DBOrCache(MenuCRUD())


@router.get('', response_model=list[MenuRead], summary='Get list of all menus')
async def read_menus(
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> list[MenuRead] | list[dict[str, str | int]]:
    return await db_loader.get_all(db, cache)


@router.get(
    '/{target_menu_id}',
    response_model=MenuRead,
    summary='Get a menu by it\'s id',
    responses={404: all_responses['menu'][404]}
)
async def read_menu_by_id(
        target_menu_id: UUID,
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> MenuRead | list[dict[str, str | int]]:
    return is_menu_none(await db_loader.get_one(db, cache, target_menu_id))


@router.post(
    '',
    response_model=Menu,
    status_code=201,
    summary='Create a new menu',
    responses={401: all_responses['menu'][401]}
)
async def create_menu(
        menu: MenuCreate,
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Menu:
    db_menu = await db_loader.create(db, cache, menu)
    if db_menu is None:
        raise HTTPException(
            status_code=401,
            detail='Menu creation error'
        )
    return db_menu


@router.patch(
    '/{target_menu_id}',
    response_model=Menu,
    summary='Update a menu',
    responses={404: all_responses['menu'][404]}
)
async def update_menu(
        target_menu_id: UUID,
        menu: MenuCreate,
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Menu | list[dict[str, str | int]]:
    return is_menu_none(await db_loader.update(db, cache, menu, target_menu_id))


@router.delete(
    '/{target_menu_id}',
    response_model=Menu,
    summary='Delete a menu',
    responses={404: all_responses['menu'][404]}
)
async def delete_menu(
        target_menu_id: UUID,
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_redis)
) -> Menu | list[dict[str, str | int]]:
    return is_menu_none(await db_loader.delete(db, cache, target_menu_id))
