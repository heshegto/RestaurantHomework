from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from ...business import schemas
from ..models import BaseModel, Dish, Menu, SubMenu


class BaseCRUDModel:
    model = BaseModel

    def _get_item_by_id(self, target_id: UUID, db: Session) -> Query:
        return db.query(self.model).filter(self.model.id == target_id).first()

    def update_item(self, target_id: UUID, update_schema: schemas.BaseCreate, db: Session) -> Query:
        item_to_update = self._get_item_by_id(target_id, db)
        if item_to_update:
            item_to_update.title = update_schema.title
            item_to_update.description = update_schema.description
            db.commit()
            db.refresh(item_to_update)
        return item_to_update

    def delete_item(self, target_id: UUID, db: Session) -> Query:
        item_to_delete = self._get_item_by_id(target_id, db)
        if item_to_delete:
            db.delete(item_to_delete)
            db.commit()
        return item_to_delete

    @staticmethod
    def commit(db_query: Menu | SubMenu | Dish, db: Session) -> None:
        db.add(db_query)
        db.commit()
        db.refresh(db_query)
