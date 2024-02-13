from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.query import Query

from app.business import schemas
from app.databases.models import BaseModel


class BaseCRUDModel:
    model = BaseModel

    async def _get_item_by_id(self, db: AsyncSession, target_id: UUID | None) -> Query:
        query = select(self.model).where(self.model.id == target_id)
        result = (await db.execute(query)).scalar()
        return result

    async def read_all_items(self, db: AsyncSession, parent_id: UUID | None) -> Query:
        query = select(self.model).where(self.model.id_parent == parent_id)
        result = (await db.execute(query)).all()
        return result

    async def read_item_by_id(
            self,
            db: AsyncSession,
            target_id: UUID | None,
            parent_id: UUID | None = None
    ) -> Query | None:
        query = select(self.model).where(self.model.id == target_id, self.model.id_parent == parent_id)
        result = (await db.execute(query)).scalar()
        return result

    async def create_item(
            self,
            db: AsyncSession,
            create_schema: schemas.BaseCreate,
            parent_id: UUID | None
    ) -> BaseModel:
        new_item = self.model(**create_schema.model_dump())
        if parent_id:
            new_item.id_parent = parent_id
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)
        return new_item

    async def update_item(
            self,
            db: AsyncSession,
            update_schema: schemas.BaseCreate,
            target_id: UUID | None
    ) -> Query | None:
        item_to_update = await self._get_item_by_id(db, target_id)
        if item_to_update:
            item_to_update.title = update_schema.title
            item_to_update.description = update_schema.description
            await db.merge(item_to_update)
            await db.commit()
            await db.refresh(item_to_update)
        return item_to_update

    async def delete_item(
            self,
            db: AsyncSession,
            target_id: UUID | None
    ) -> Query | None:
        item_to_delete = await self._get_item_by_id(db, target_id)
        if item_to_delete:
            await db.delete(item_to_delete)
            await db.commit()
        return item_to_delete
