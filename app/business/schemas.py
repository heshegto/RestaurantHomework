from uuid import UUID

from pydantic import BaseModel, field_validator

"""
Read schemas are used only for reading. Create schemas are used to validate creation data in creation moment.
Schemas without anything are used as response models.
"""


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

    @field_validator('price')
    def validate_price(cls, value: str) -> str:
        return f'{round(float(value), 2):.2f}'
