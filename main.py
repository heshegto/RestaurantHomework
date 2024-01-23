from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import get_db, engine

from uuid import UUID

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


''' ----- Menu API ----- '''


@app.get('/api/v1/menus', response_model=list[schemas.Menu])
def read_menus(db: Session = Depends(get_db)):
    return crud.get_menus(db)


@app.get('/api/v1/menus/{target_menu_id}', response_model=schemas.Menu)
def read_menu_by_id(target_menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, target_menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu


@app.post('/api/v1/menus', response_model=schemas.Menu, status_code=201)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    return crud.create_menu(db, menu)


@app.patch('/api/v1/menus/{target_menu_id}', response_model=schemas.Menu)
def update_menu(target_menu_id: UUID, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    return crud.patch_menu(db, target_menu_id, menu)


@app.delete('/api/v1/menus/{target_menu_id}', response_model=schemas.Menu)
def delete_menu(target_menu_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_menu(db, target_menu_id)


''' ----- SubMenu API ----- '''


@app.get('/api/v1/menus/{target_menu_id}/submenus', response_model=list[schemas.SubMenu])
def read_submenus(target_menu_id: UUID, db: Session = Depends(get_db)):
    return crud.get_submenus(db, target_menu_id)


@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.SubMenu)
def read_submenu_by_id(target_submenu_id: UUID, target_menu_id: UUID, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu_by_id(db, target_submenu_id, target_menu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu


@app.post('/api/v1/menus/{target_menu_id}/submenus', response_model=schemas.SubMenu, status_code=201)
def create_submenu(target_menu_id: UUID, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)):
    return crud.create_submenu(db, target_menu_id, submenu)


@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.SubMenu)
def update_submenu(target_submenu_id: UUID, target_menu_id: UUID, submenu: schemas.SubMenuCreate,
                   db: Session = Depends(get_db)):
    return crud.patch_submenu(db, target_submenu_id, target_menu_id, submenu)


@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.SubMenu)
def delete_submenu(target_submenu_id: UUID, target_menu_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_submenu(db, target_submenu_id, target_menu_id)


''' ----- Dish API ----- '''


@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', response_model=list[schemas.Dish])
def read_dishes(target_submenu_id: UUID, db: Session = Depends(get_db)):
    return crud.get_dishes(db, target_submenu_id)


@app.get(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
    response_model=schemas.Dish
)
def read_dish_by_id(target_dish_id: UUID, target_submenu_id: UUID, db: Session = Depends(get_db)):
    db_dish = crud.get_dish_by_id(db, target_dish_id, target_submenu_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish


@app.post(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
    response_model=schemas.Dish,
    status_code=201
)
def create_dish(
        target_submenu_id: UUID,
        target_menu_id: UUID,
        dish: schemas.DishCreate,
        db: Session = Depends(get_db)
):
    return crud.create_dish(db, target_submenu_id, target_menu_id, dish)


@app.patch(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
    response_model=schemas.Dish
)
def update_dish(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        dish: schemas.DishCreate,
        db: Session = Depends(get_db)
):
    return crud.patch_dish(db, target_dish_id, target_submenu_id, dish)


@app.delete(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
    response_model=schemas.Dish
)
def delete_dish(
        target_dish_id: UUID,
        target_submenu_id: UUID,
        target_menu_id: UUID,
        db: Session = Depends(get_db)
):
    return crud.delete_dish(db, target_dish_id, target_submenu_id, target_menu_id)
