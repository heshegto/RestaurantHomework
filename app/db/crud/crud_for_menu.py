from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.business import schemas
from app.db import models


def get_menus(db: Session):
    return db.query(
        models.Menu.id,
        models.Menu.title,
        models.Menu.description,
        func.count(func.distinct(models.SubMenu.id)).label('submenus_count'),
        func.count(models.Dish.id).label('dishes_count'),
    ).outerjoin(models.SubMenu, models.Menu.child_menu
                ).outerjoin(models.Dish, models.SubMenu.dish
                            ).group_by(models.Menu.id)


def get_menu_by_id(db: Session, menu_id: UUID):
    return get_menus(db).filter(models.Menu.id == menu_id).first()


def __get_menu_by_id(db: Session, menu_id: UUID):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(title=menu.title, description=menu.description)

    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)

    return db_menu


def patch_menu(db: Session, menu_id: UUID, menu: schemas.MenuCreate):
    menu_to_update = __get_menu_by_id(db, menu_id)
    if menu_to_update:
        menu_to_update.title = menu.title
        menu_to_update.description = menu.description
        db.commit()
        db.refresh(menu_to_update)
    return menu_to_update


def delete_menu(db: Session, menu_id: UUID):
    menu_to_delete = __get_menu_by_id(db, menu_id)
    if menu_to_delete:
        db.delete(menu_to_delete)
        db.commit()
    return menu_to_delete
