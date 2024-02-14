from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.query import Query

from app.databases.models import Menu, SubMenu


async def read_everything(db: AsyncSession) -> Query:
    query = select(Menu).options(selectinload(Menu.child_menu).options(selectinload(SubMenu.dish)))
    result = (await db.execute(query)).scalars().fetchall()
    return result
