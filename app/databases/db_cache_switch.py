from uuid import UUID

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from app.business.schemas import (
    Dish,
    DishCreate,
    Menu,
    MenuCreate,
    MenuRead,
    SubMenu,
    SubMenuCreate,
    SubMenuRead,
)

from .cache import crud as cache_crud
from .cache.cache import get_redis
from .cache.cache_keys import CacheKeys
from .db.crud import DishCRUD, MenuCRUD, SubMenuCRUD, read_everything
from .db.database import get_db


class DBOrCache:
    def __init__(self, db_crud_type: MenuCRUD | SubMenuCRUD | DishCRUD) -> None:
        self.db_crud = db_crud_type
        self.cache_keys = CacheKeys(db_crud_type)

    async def get_all(
            self,
            db: AsyncSession = Depends(get_db),
            cache: Redis = Depends(get_redis),
            parent_id: UUID | None = None,
            grand_id: UUID | None = None,
    ) -> list[MenuRead] | list[SubMenuRead] | list[Dish] | list[dict[str, str | int]] | Query:
        keyword = self.cache_keys.get_required_keys(parent_id, grand_id)[-3]
        data = cache_crud.read_cache(keyword, cache)
        if data:
            return data
        items = await self.db_crud.read_all_items(db, parent_id)

        # for item in items:
        #     keyword_ = str(item.id) + ':sale'
        #     data = cache_crud.read_cache(keyword_, cache)
        #     if data:
        #         item = jsonable_encoder(item.scalar())
        #         item["sale"] = data
        #         item["price"] = item["price"] * (1 - int(data))

        cache_crud.create_cache(keyword, items, cache)
        return items

    async def get_one(
            self,
            db: AsyncSession = Depends(get_db),
            cache: Redis = Depends(get_redis),
            target_id: UUID | None = None,
            parent_id: UUID | None = None,
            grand_id: UUID | None = None
    ) -> MenuRead | SubMenuRead | Dish | list[dict[str, str | int]] | None:
        keyword = self.cache_keys.get_required_keys(target_id, parent_id, grand_id)[-2]
        data = cache_crud.read_cache(keyword, cache)
        if data:
            return data
        items = await self.db_crud.read_item_by_id(db, target_id, parent_id)

        keyword_ = str(target_id) + ':sale'
        data = cache_crud.read_cache(keyword_, cache)
        if data:
            items = jsonable_encoder(items.scalar())
            items["sale"] = data
            items["price"] = items["price"] * (1-int(data))

        cache_crud.create_cache(keyword, items, cache)
        return items

    async def create(
            self,
            db: AsyncSession = Depends(get_db),
            schema: DishCreate | SubMenuCreate | MenuCreate = DishCreate(),
            parent_id: UUID | None = None,
    ) -> Menu | SubMenu | Dish | None:
        return await self.db_crud.create_item(db, schema, parent_id)

    async def update(
            self,
            db: AsyncSession = Depends(get_db),
            schema: DishCreate | SubMenuCreate | MenuCreate = DishCreate(),
            target_id: UUID | None = None,
    ) -> Menu | SubMenu | Dish | None:
        return await self.db_crud.update_item(db, schema, target_id)

    async def delete(
            self,
            db: AsyncSession = Depends(get_db),
            target_id: UUID | None = None,
    ) -> Menu | SubMenu | Dish | None:
        return await self.db_crud.delete_item(db, target_id)

    @staticmethod
    async def get_everything(
            db: AsyncSession = Depends(get_db),
            cache: Redis = Depends(get_redis),
    ) -> list[MenuRead] | list[SubMenuRead] | list[Dish] | list[dict[str, str | int]] | Query:
        keyword = 'everything'
        data = cache_crud.read_cache(keyword, cache)
        if data:
            return data
        items = await read_everything(db)
        cache_crud.create_cache(keyword, items, cache)
        return items
