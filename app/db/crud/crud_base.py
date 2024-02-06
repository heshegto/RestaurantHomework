from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from ...business import schemas
from ..models import BaseModel, Dish, Menu, SubMenu


class BaseCRUDModel:
    model = BaseModel

    def _get_item_by_id(self, db: Session, target_id: UUID | None) -> Query:
        return db.query(self.model).filter(self.model.id == target_id)

    def read_all_items(self, db: Session, parent_id: UUID | None) -> Query:
        return db.query(self.model).filter(self.model.id_parent == parent_id)

    def read_item_by_id(self, db: Session, target_id: UUID | None, parent_id: UUID | None = None) -> Query | None:
        return self.read_all_items(db, parent_id).filter(self.model.id == target_id)

    def create_item(self, db: Session, create_schema: schemas.BaseCreate, parent_id: UUID | None) -> BaseModel:
        db_dish = self.model(**create_schema.model_dump())
        if parent_id:
            db_dish.id_parent = parent_id
        self.commit(db, db_dish)
        return db_dish

    def update_item(self, db: Session, update_schema: schemas.BaseCreate, target_id: UUID | None) -> BaseModel:
        item_to_update = self._get_item_by_id(db, target_id).first()
        if item_to_update:
            item_to_update.title = update_schema.title
            item_to_update.description = update_schema.description
            db.commit()
            db.refresh(item_to_update)
        return item_to_update

    def delete_item(self, db: Session, target_id: UUID | None) -> BaseModel:
        item_to_delete = self._get_item_by_id(db, target_id).first()
        if item_to_delete:
            db.delete(item_to_delete)
            db.commit()
        return item_to_delete

    @staticmethod
    def commit(db: Session, db_query: Menu | SubMenu | Dish) -> None:
        db.add(db_query)
        db.commit()
        db.refresh(db_query)
