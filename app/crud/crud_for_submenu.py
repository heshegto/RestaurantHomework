from sqlalchemy.orm import Session
from app import models, schemas
from uuid import UUID
from .crud_for_menu import get_menu_by_id


def get_submenus(db: Session, menu_id: UUID):
    return db.query(models.SubMenu).filter(models.SubMenu.id_menu == menu_id).all()


def get_submenu_by_id(db: Session, submenu_id: UUID, menu_id: UUID):
    return db.query(models.SubMenu).filter(
        (models.SubMenu.id == submenu_id) & (models.SubMenu.id_menu == menu_id)
    ).first()


def create_submenu(db: Session, menu_id: UUID, submenu: schemas.SubMenuCreate):
    db_submenu = models.SubMenu(title=submenu.title, description=submenu.description, id_menu=menu_id)
    db.add(db_submenu)

    parent_menu = get_menu_by_id(db, menu_id)
    parent_menu.submenus_count += 1

    db.commit()
    db.refresh(db_submenu)

    return db_submenu


def patch_submenu(db: Session, submenu_id: UUID, menu_id: UUID, submenu: schemas.SubMenuCreate):
    submenu_to_update = get_submenu_by_id(db, submenu_id, menu_id)
    if submenu_to_update:
        submenu_to_update.title = submenu.title
        submenu_to_update.description = submenu.description
        db.commit()
        db.refresh(submenu_to_update)
    return submenu_to_update


def delete_submenu(db: Session, submenu_id: UUID, menu_id: UUID):
    submenu_to_delete = get_submenu_by_id(db, submenu_id, menu_id)
    if submenu_to_delete:
        parent_menu = get_menu_by_id(db, menu_id)
        parent_menu.submenus_count -= 1
        parent_menu.dishes_count -= submenu_to_delete.dishes_count

        db.delete(submenu_to_delete)
        db.commit()
    return submenu_to_delete
