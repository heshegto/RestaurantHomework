from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from ...business import schemas
from ..models import Dish
from .crud_base import BaseCRUDModel


class DishCRUD(BaseCRUDModel):
    def __init__(self) -> None:
        self.model = Dish

    def create_item(self, submenu_id: UUID, dish: schemas.DishCreate, db: Session) -> Query:
        db_dish = self.model(
            title=dish.title,
            description=dish.description,
            price=f'{round(float(dish.price), 2):.2f}',
            id_submenu=submenu_id
        )
        db.add(db_dish)
        db.commit()
        return db_dish

    def read_all_items(self, submenu_id: UUID, db: Session) -> Query:
        return db.query(self.model).filter(self.model.id_submenu == submenu_id)

    def read_item_by_id(self, target_id: UUID, parent_id: UUID, db: Session) -> Query:
        return self.read_all_items(parent_id, db).filter(self.model.id == target_id)

    def update_item(self, target_id: UUID, dish: schemas.DishCreate, db: Session) -> list[dict] | None:
        dish_to_update = super()._get_item_by_id(target_id, db)
        if dish_to_update:
            dish_to_update.title = dish.title
            dish_to_update.description = dish.description
            dish_to_update.price = f'{round(float(dish.price), 2):.2f}'
            db.commit()
            db.refresh(dish_to_update)
        return dish_to_update
