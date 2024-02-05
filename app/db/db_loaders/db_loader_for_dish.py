from uuid import UUID

from redis import Redis
from sqlalchemy.orm import Session

from ...business import schemas
from .. import cache_database
from ..crud.crud_for_dish import DishCRUD


class DishLoader:
    crud = DishCRUD()

    def get_all_dishes(self, submenu_id: UUID, menu_id: UUID, db: Session, cache: Redis):
        keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dishes'
        data = cache_database.read_cache(keyword, cache)
        if data:
            return data
        items = self.crud.read_all_items(submenu_id, db).all()
        cache_database.create_cache(keyword, items, cache)
        return items

    def get_one_dish(self, dish_id: UUID, submenu_id: UUID, menu_id: UUID, db: Session, cache: Redis):
        keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dish:{str(dish_id)}'
        data = cache_database.read_cache(keyword, cache)
        if data:
            return data
        items = self.crud.read_item_by_id(dish_id, db)
        cache_database.create_cache(keyword, items, cache)
        return items

    def create_dish(self, submenu_id: UUID, menu_id: UUID, dish: schemas.DishCreate, db: Session, cache: Redis):
        keywords = [
            'menus',
            f'menu:{str(menu_id)}',
            f'menu:{str(menu_id)}:submenus',
            f'menu:{str(menu_id)}:submenu:{str(submenu_id)}'
            f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dishes',
        ]
        cache_database.delete_cache(keywords, cache=cache)
        return self.crud.create_item(submenu_id, dish, db)

    def update_dish(self, dish_id: UUID, submenu_id: UUID, menu_id: UUID, dish: schemas.DishCreate, db: Session,
                    cache: Redis):
        keywords = [
            'menus',
            f'menu:{str(menu_id)}',
            f'menu:{str(menu_id)}:submenus',
            f'menu:{str(menu_id)}:submenu:{str(submenu_id)}'
            f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dishes',
            f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dish:{str(dish_id)}'
        ]
        cache_database.delete_cache(keywords, cache=cache)
        return self.crud.update_item(dish_id, dish, db)

    def delete_dish(self, dish_id: UUID, submenu_id: UUID, menu_id: UUID, db: Session, cache: Redis):
        keywords = [
            'menus',
            f'menu:{str(menu_id)}',
            f'menu:{str(menu_id)}:submenus',
            f'menu:{str(menu_id)}:submenu:{str(submenu_id)}'
            f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dishes',
            f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:dish:{str(dish_id)}'
        ]
        cache_database.delete_cache(keywords, cache=cache)
        return self.crud.delete_item(dish_id, db)
