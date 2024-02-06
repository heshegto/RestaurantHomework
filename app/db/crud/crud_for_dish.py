from uuid import UUID

from sqlalchemy.orm import Session

from ...business import schemas
from ..models import Dish
from .crud_base import BaseCRUDModel


class DishCRUD(BaseCRUDModel):
    def __init__(self) -> None:
        self.model = Dish

    def update_item(self, db: Session, dish: schemas.DishCreate, target_id: UUID | None) -> Dish:
        dish_to_update = super()._get_item_by_id(db, target_id).first()
        if dish_to_update:
            dish_to_update.title = dish.title
            dish_to_update.description = dish.description
            dish_to_update.price = f'{round(float(dish.price), 2):.2f}'
            db.commit()
            db.refresh(dish_to_update)
        return dish_to_update
