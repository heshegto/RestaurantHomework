from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.query import Query

from app.databases.models import Dish

from .crud_base import BaseCRUDModel


class DishCRUD(BaseCRUDModel):
    """Class for CRUD operations on Dishes"""
    def __init__(self) -> None:
        self.model = Dish

    async def read_all_items(self, db: AsyncSession, parent_id: UUID | None = None) -> Query:
        """Returns all Dishes in the database for a given SubMenu id."""
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            self.model.price
        ).where(self.model.id_parent == parent_id)
        result = (await db.execute(query)).all()
        return result

    async def read_item_by_id(self, db: AsyncSession, target_id: UUID, parent_id: UUID | None = None) -> Query | None:
        """Returns a single Dish from the database for a given Dish and SubMenu id's."""
        query = select(self.model).where(self.model.id == target_id, self.model.id_parent == parent_id)
        result = (await db.execute(query)).scalar()
        return result
