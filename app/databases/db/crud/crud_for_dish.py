from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from sqlalchemy.orm.query import Query

from app.business import schemas
from app.databases.models import Dish
from .crud_base import BaseCRUDModel


class DishCRUD(BaseCRUDModel):
    def __init__(self) -> None:
        self.model = Dish

    async def read_all_items(self, db: AsyncSession, parent_id: UUID | None) -> Query:
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.price
        ).where(self.model.id_parent == parent_id)
        result = (await db.execute(query)).all()
        return result

    async def update_item(self, db: AsyncSession, dish: schemas.DishCreate, target_id: UUID | None) -> Dish | None:
        dish_to_update = await super()._get_item_by_id(db, target_id)
        if dish_to_update:
            dish_to_update.title = dish.title
            dish_to_update.description = dish.description
            dish_to_update.price = f'{round(float(dish.price), 2):.2f}'
            await db.merge(dish_to_update)
            await db.commit()
            await db.refresh(dish_to_update)
        return dish_to_update
