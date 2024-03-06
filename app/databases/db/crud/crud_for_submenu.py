from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.query import Query

from app.databases.models import Dish, SubMenu

from .crud_base import BaseCRUDModel


class SubMenuCRUD(BaseCRUDModel):
    """Class for CRUD operations on SubMenus"""
    def __init__(self) -> None:
        self.model = SubMenu

    async def read_all_items(self, db: AsyncSession, parent_id: UUID | None = None) -> Query:
        """Returns all SubMenus in the database for a given Menu id."""
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            func.count(Dish.id).label('dishes_count'),
        ).outerjoin(Dish, self.model.dish
                    ).where(self.model.id_parent == parent_id
                            ).group_by(self.model.id)
        result = (await db.execute(query)).all()
        return result

    async def read_item_by_id(self, db: AsyncSession, target_id: UUID, parent_id: UUID | None = None) -> Query | None:
        """Returns a single SubMenu from the database for a given SubMenu and Menu id's."""
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            func.count(Dish.id).label('dishes_count'),
        ).outerjoin(Dish, self.model.dish
                    ).where(self.model.id_parent == parent_id and self.model.id == target_id
                            ).group_by(self.model.id)
        result = (await db.execute(query)).first()
        return result
