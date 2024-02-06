from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from ..models import Dish, Menu, SubMenu
from .crud_base import BaseCRUDModel


class MenuCRUD(BaseCRUDModel):
    def __init__(self) -> None:
        self.model = Menu

    def read_all_items(self, db: Session, parent_id: UUID | None) -> Query:
        return db.query(
            self.model.id,
            self.model.title,
            self.model.description,
            func.count(func.distinct(SubMenu.id)).label('submenus_count'),
            func.count(Dish.id).label('dishes_count'),
        ).outerjoin(SubMenu, self.model.child_menu
                    ).outerjoin(Dish, SubMenu.dish
                                ).group_by(self.model.id)
