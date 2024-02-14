from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.query import Query

from app.databases.models import Dish, Menu, SubMenu

from .crud_base import BaseCRUDModel


class MenuCRUD(BaseCRUDModel):
    def __init__(self) -> None:
        self.model = Menu

    async def read_all_items(self, db: AsyncSession, parent_id: UUID | None) -> Query:
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            func.count(func.distinct(SubMenu.id)).label('submenus_count'),
            func.count(Dish.id).label('dishes_count'),
        ).outerjoin(SubMenu, self.model.child_menu
                    ).outerjoin(Dish, SubMenu.dish
                                ).group_by(self.model.id)
        result = (await db.execute(query)).all()
        return result

    async def read_item_by_id(
            self,
            db: AsyncSession,
            target_id: UUID | None,
            parent_id: UUID | None = None
    ) -> Query | None:
        query = select(
            self.model.id,
            self.model.title,
            self.model.description,
            func.count(func.distinct(SubMenu.id)).label('submenus_count'),
            func.count(Dish.id).label('dishes_count'),
        ).outerjoin(SubMenu, self.model.child_menu
                    ).outerjoin(Dish, SubMenu.dish
                                ).where(self.model.id == target_id).group_by(self.model.id)
        result = (await db.execute(query)).first()
        return result
