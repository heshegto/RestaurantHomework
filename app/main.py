from fastapi import FastAPI

from .db import models
from .db.database import engine
from .business.handlers import menu_router, submenu_router, dish_router


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
