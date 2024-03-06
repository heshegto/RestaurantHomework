from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.query import Query

from app.business.schemas import BaseCreate as CreateSchema
from app.databases.models import BaseModel


class BaseCRUDModel:
    """Base class for almost every CRUD operations. Can't be used directly, always create subclasses"""
    __abstract__ = True

    def __init__(self) -> None:
        """
            Saves model type for future database work. \n
            Should be overridden by subclasses!!!
        """
        self.model = BaseModel
        raise NotImplementedError(f'You must implement __init__ method for model {self.model.__name__}')

    async def read_all_items(self, db: AsyncSession, parent_id: UUID | None = None) -> Query:
        """
            Returns all items of specific type from the database. \n
            Should be overridden by subclasses!!!
        """
        raise NotImplementedError(f'You must implement read_all_items method for model {self.model.__name__}')

    async def read_item_by_id(self, db: AsyncSession, target_id: UUID, parent_id: UUID | None = None) -> Query | None:
        """
            Returns only one item of specific type by id from the database. \n
            Should be overridden by subclasses!!!
        """
        raise NotImplementedError(f'You must implement read_item_by_id method for model {self.model.__name__}')

    async def create_item(self, db: AsyncSession, create_schema: CreateSchema, parent_id: UUID | None) -> Query:
        """Creates new item in database."""
        new_item = self.model(**create_schema.model_dump())
        if parent_id:
            new_item.id_parent = parent_id
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)
        return new_item

    async def __get_item_by_id(self, db: AsyncSession, target_id: UUID) -> Query | None:
        """Searches items by id for update and delete methods of this class"""
        query = select(self.model).where(self.model.id == target_id)
        result = (await db.execute(query)).scalar()
        return result

    async def update_item(self, db: AsyncSession, update_schema: CreateSchema, target_id: UUID) -> Query | None:
        """Updates item in database using id and given update_schema"""
        item_to_update = await self.__get_item_by_id(db, target_id)
        if item_to_update:
            item_to_update.title = update_schema.title
            item_to_update.description = update_schema.description
            if update_schema.price is not None:
                item_to_update.price = update_schema.price
            await db.merge(item_to_update)
            await db.commit()
            await db.refresh(item_to_update)
        return item_to_update

    async def delete_item(self, db: AsyncSession, target_id: UUID) -> Query | None:
        """Deletes item from database by id"""
        item_to_delete = await self.__get_item_by_id(db, target_id)
        if item_to_delete:
            await db.delete(item_to_delete)
            await db.commit()
        return item_to_delete
