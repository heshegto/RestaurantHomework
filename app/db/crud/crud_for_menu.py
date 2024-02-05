from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from ...business import schemas
from ..models import Dish, Menu, SubMenu
from .crud_base import BaseCRUDModel


class MenuCRUD(BaseCRUDModel):
    def __init__(self) -> None:
        self.model = Menu

    def create_item(self, menu: schemas.MenuCreate, db: Session) -> Query:
        db_menu = self.model(title=menu.title, description=menu.description)
        self.commit(db_menu, db)
        return db_menu

    def read_all_items(self, db: Session) -> Query:
        return db.query(
            self.model.id,
            self.model.title,
            self.model.description,
            func.count(func.distinct(SubMenu.id)).label('submenus_count'),
            func.count(Dish.id).label('dishes_count'),
        ).outerjoin(SubMenu, self.model.child_menu
                    ).outerjoin(Dish, SubMenu.dish
                                ).group_by(self.model.id)

    def read_item_by_id(self, target_id: UUID, db: Session) -> Query:
        return self.read_all_items(db).filter(self.model.id == target_id)
