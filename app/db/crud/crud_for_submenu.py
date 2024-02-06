from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from ..models import Dish, SubMenu
from .crud_base import BaseCRUDModel


class SubMenuCRUD(BaseCRUDModel):
    def __init__(self) -> None:
        self.model = SubMenu

    def read_all_items(self, db: Session, parent_id: UUID | None) -> Query:
        return db.query(
            self.model.id,
            self.model.title,
            self.model.description,
            func.count(Dish.id).label('dishes_count'),
        ).outerjoin(Dish, self.model.dish
                    ).filter(self.model.id_parent == parent_id
                             ).group_by(self.model.id)
