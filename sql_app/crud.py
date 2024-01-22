from sqlalchemy.orm import Session
from . import models, schemas
from uuid import UUID
from sqlalchemy import func


# ----- CRUD for Menu


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


# ----- CRUD for SubMenu -----


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


# ----- CRUD for Dishes -----


def get_dishes(db: Session, target_submenu_id: UUID):
    return db.query(models.Dish).filter(models.Dish.id_submenu == target_submenu_id).all()


def create_dish(db: Session, submenu_id: UUID, menu_id: UUID, dish: schemas.DishCreate):
    db_dish = models.Dish(
        title=dish.title,
        description=dish.description,
        price="{:.2f}".format(round(float(dish.price), 2)),
        id_submenu=submenu_id
    )
    db.add(db_dish)

    get_submenu_by_id(db, submenu_id, menu_id).dishes_count += 1
    get_menu_by_id(db, menu_id).dishes_count += 1

    db.commit()
    db.refresh(db_dish)

    return db_dish


def get_dish_by_id(db: Session, target_dish_id: UUID, target_submenu_id: UUID):
    return db.query(models.Dish).filter(
        (models.Dish.id == target_dish_id) & (models.Dish.id_submenu == target_submenu_id)
    ).first()


def patch_dish(db: Session, target_dish_id: UUID, target_submenu_id: UUID, dish: schemas.DishCreate):
    dish_to_update = get_dish_by_id(db, target_dish_id, target_submenu_id)
    if dish_to_update:
        dish_to_update.title = dish.title
        dish_to_update.description = dish.description
        dish_to_update.price = "{:.2f}".format(round(float(dish.price), 2))
        db.commit()
        db.refresh(dish_to_update)
    return dish_to_update


def delete_dish(db: Session, dish_id: UUID, submenu_id: UUID, menu_id: UUID):
    dish_to_delete = get_dish_by_id(db, dish_id, submenu_id)
    if dish_to_delete:
        db.delete(dish_to_delete)
        get_submenu_by_id(db, submenu_id, menu_id).dishes_count -= 1
        get_menu_by_id(db, menu_id).dishes_count -= 1
        db.commit()
    return dish_to_delete
