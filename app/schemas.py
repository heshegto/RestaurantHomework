from pydantic import BaseModel
from uuid import UUID


class BaseCreate(BaseModel):
    title: str
    description: str | None = None


class Base(BaseCreate):
    id: UUID


class Menu(Base):
    pass


class MenuCreate(BaseCreate):
    pass


class MenuRead(Menu):
    submenus_count: int = 0
    dishes_count: int = 0


class SubMenu(Base):
    pass


class SubMenuCreate(BaseCreate):
    pass


class SubMenuRead(SubMenu):
    dishes_count: int = 0


class Dish(Base):
    price: str


class DishCreate(BaseCreate):
    price: str
