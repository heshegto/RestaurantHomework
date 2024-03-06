import uuid

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .db.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)


class Menu(BaseModel):
    __tablename__ = 'menus'

    submenu = relationship('SubMenu', back_populates='menu', cascade='all, delete')


class SubMenu(BaseModel):
    __tablename__ = 'submenus'

    id_parent = Column(UUID(as_uuid=True), ForeignKey('menus.id', ondelete='CASCADE'))

    menu = relationship('Menu', back_populates='submenu')
    dish = relationship('Dish', back_populates='submenu', cascade='all, delete')


class Dish(BaseModel):
    __tablename__ = 'dishes'

    price = Column(String)
    id_parent = Column(UUID(as_uuid=True), ForeignKey('submenus.id', ondelete='CASCADE'))

    submenu = relationship('SubMenu', back_populates='dish')
