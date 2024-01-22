from pydantic import BaseModel
from uuid import UUID


class BaseCreate(BaseModel):
    title: str
    description: str | None = None


class Base(BaseCreate):
    id: UUID


class Menu(Base):
    submenus_count: int = 0
    dishes_count: int = 0


class MenuCreate(BaseCreate):
    pass


class SubMenu(Base):
    dishes_count: int = 0


class SubMenuCreate(BaseCreate):
    pass


class Dish(Base):
    price: str


class DishCreate(BaseCreate):
    price: str
