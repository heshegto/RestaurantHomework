from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from ...business import schemas
from ..models import Dish, SubMenu
from .crud_base import BaseCRUDModel


class SubMenuCRUD(BaseCRUDModel):
    def __init__(self) -> None:
        self.model = SubMenu

    def create_item(self, submenu: schemas.SubMenuCreate, parent_id: UUID, db: Session) -> Query:
        db_submenu = self.model(title=submenu.title, description=submenu.description, id_menu=parent_id)
        self.commit(db_submenu, db)
        return db_submenu

    def read_all_items(self, parent_id: UUID, db: Session) -> Query:
        return db.query(
            self.model.id,
            self.model.title,
            self.model.description,
            func.count(Dish.id).label('dishes_count'),
        ).outerjoin(Dish, self.model.dish
                    ).filter(self.model.id_menu == parent_id
                             ).group_by(self.model.id)

    def read_item_by_id(self, target_id: UUID, parent_id: UUID, db: Session) -> Query:
        return self.read_all_items(parent_id, db).filter(self.model.id == target_id)
