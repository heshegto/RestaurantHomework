from sqlalchemy.orm import Session
from app import models, schemas
from uuid import UUID


def get_menus(db: Session):
    return db.query(models.Menu).all()


def get_menu_by_id(db: Session, menu_id: UUID):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(title=menu.title, description=menu.description)

    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)

    return db_menu


def patch_menu(db: Session, menu_id: UUID, menu: schemas.MenuCreate):
    menu_to_update = get_menu_by_id(db, menu_id)
    if menu_to_update:
        menu_to_update.title = menu.title
        menu_to_update.description = menu.description
        db.commit()
        db.refresh(menu_to_update)
    return menu_to_update


def delete_menu(db: Session, menu_id: UUID):
    menu_to_delete = get_menu_by_id(db, menu_id)
    if menu_to_delete:
        db.delete(menu_to_delete)
        db.commit()
    return menu_to_delete