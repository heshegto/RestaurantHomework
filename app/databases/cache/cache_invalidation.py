from uuid import UUID

from redis import Redis
from fastapi import Depends
from app.databases.cache.cache import get_redis
from app.databases.cache import crud as cache_crud
from app.databases.cache.cache_keys import CacheKeys
from app.databases.db.crud import DishCRUD, MenuCRUD, SubMenuCRUD


def invalidation_on_creation(
        cache: Redis = Depends(get_redis),
        parent_id: UUID | None = None,
        grand_id: UUID | None = None,
) -> None:
    keywords = get_keys_for_item_type(parent_id, grand_id).get_required_keys(parent_id, grand_id)[:-2] + ['everything']
    cache_crud.delete_cache(keywords, cache=cache)


def invalidation_on_update(
        cache: Redis = Depends(get_redis),
        target_id: UUID | None = None,
        parent_id: UUID | None = None,
        grand_id: UUID | None = None,
) -> None:
    keywords = get_keys_for_item_type(parent_id, grand_id).get_required_keys(
        target_id,
        parent_id,
        grand_id
    )[-3:-1] + ['everything']
    cache_crud.delete_cache(keywords, cache=cache)


def invalidation_on_delete(
        cache: Redis = Depends(get_redis),
        target_id: UUID | None = None,
        parent_id: UUID | None = None,
        grand_id: UUID | None = None,
) -> None:
    keywords = get_keys_for_item_type(parent_id, grand_id).get_required_keys(
        target_id,
        parent_id,
        grand_id
    ) + ['everything']
    cache_crud.delete_cache(keywords, cache=cache)


def get_keys_for_item_type(parent_id: UUID | None = None, grand_id: UUID | None = None) -> CacheKeys:
    if grand_id:
        return CacheKeys(DishCRUD())
    elif parent_id:
        return CacheKeys(SubMenuCRUD())
    else:
        return CacheKeys(MenuCRUD())
