from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.query import Query

from app.business import schemas
from app.databases.models import BaseModel


async def read_all_items(self, db: AsyncSession, parent_id: UUID | None) -> Query:
    query = self.get_all_items_query().where(self.model.id_parent == parent_id)
    result = (await db.execute(query)).all()
    return result