from fastapi import APIRouter, Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.cache.cache import get_redis
from app.databases.db.crud import DishCRUD
from app.databases.db.database import get_db
from app.databases.db_cache_switch import DBOrCache

router = APIRouter(prefix='/api/v1/everything', tags=['Everything'])
db_loader = DBOrCache(DishCRUD())


@router.get('', summary='Get everything')
async def read_everything(
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_redis)
):
    return await db_loader.get_everything(db, cache)
