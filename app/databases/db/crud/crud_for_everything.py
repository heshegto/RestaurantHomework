
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.query import Query

from app.databases.models import Dish, Menu, SubMenu


async def read_everything(db: AsyncSession) -> Query:
    query = select(Menu, SubMenu, Dish).join(SubMenu, Menu.child_menu
                                             ).join(Dish, SubMenu.dish
                                                    )
    result = (await db.execute(query)).all()
    return result
