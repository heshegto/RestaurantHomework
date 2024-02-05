from fastapi import FastAPI

from .business.handlers import dish_router, menu_router, submenu_router
from .db import models
from .db.database import engine

models.Base.metadata.create_all(bind=engine)

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

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
