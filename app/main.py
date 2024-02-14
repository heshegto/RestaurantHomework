from fastapi import FastAPI

from .business.handlers import dish_router, menu_router, submenu_router, all_router
from .databases import models
from .databases.db.database import engine
from .databases.cache.cache import get_redis
# from .background_tasks.tasks import synchronization
# from .tasks.tasks import update_base

app = FastAPI(
    title='Restaurant API',
    description='App for restaurant',
    version='3.4.0',
    openapi_tags=[
        {
            'name': 'Menu',
            'description': 'Menu related operations',
        },
        {
            'name': 'Submenu',
            'description': 'Submenu related operations',
        },
        {
            'name': 'Dish',
            'description': 'Dish related operations',
        },
    ]
)


@app.on_event("startup")
async def init_tables() -> None:
    red = get_redis()
    red.flushdb()
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    # synchronization.delay()


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
app.include_router(all_router)
