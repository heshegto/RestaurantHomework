from uuid import UUID

from redis import Redis
from sqlalchemy.orm import Session

from ...business.schemas import (
    Dish,
    DishCreate,
    Menu,
    MenuCreate,
    MenuRead,
    SubMenu,
    SubMenuCreate,
    SubMenuRead,
)
from .. import cache_database
from ..crud import DishCRUD, MenuCRUD, SubMenuCRUD
from .keywords import dish_keywords, menu_keywords, submenu_keywords


class BaseLoader:
    def __init__(self, crud: MenuCRUD | SubMenuCRUD | DishCRUD):
        self.crud = crud

    def get_all(
            self,
            db: Session,
            cache: Redis,
            parent_id: UUID | None = None,
            grand_id: UUID | None = None,
    ) -> list[MenuRead] | list[SubMenuRead] | list[Dish] | list[dict[str, str | int]]:
        keyword = self.__get_required_keywords(parent_id, grand_id)[-3]
        data = cache_database.read_cache(keyword, cache)
        if data:
            return data
        items = self.crud.read_all_items(db, parent_id).all()
        cache_database.create_cache(keyword, items, cache)
        return items

    def get_one(
            self,
            db: Session,
            cache: Redis,
            target_id: UUID | None = None,
            parent_id: UUID | None = None,
            grand_id: UUID | None = None
    ) -> MenuRead | SubMenuRead | Dish | list[dict[str, str | int]] | None:
        keyword = self.__get_required_keywords(target_id, parent_id, grand_id)[-2]
        data = cache_database.read_cache(keyword, cache)
        if data:
            return data
        items = self.crud.read_item_by_id(db, target_id, parent_id)
        if items is None:
            return None
        items = items.first()
        cache_database.create_cache(keyword, items, cache)
        return items

    def create(
            self,
            db: Session,
            cache: Redis,
            schema: DishCreate | SubMenuCreate | MenuCreate,
            parent_id: UUID | None = None,
            grand_id: UUID | None = None,
    ) -> Menu | SubMenu | Dish | None:
        keywords = self.__get_required_keywords(parent_id, grand_id)[:-2]
        cache_database.delete_cache(keywords, cache=cache)
        return self.crud.create_item(db, schema, parent_id)

    def update(
            self,
            db: Session,
            cache: Redis,
            schema: DishCreate | SubMenuCreate | MenuCreate,
            target_id: UUID | None = None,
            parent_id: UUID | None = None,
            grand_id: UUID | None = None,
    ) -> Menu | SubMenu | Dish | None:
        keywords = self.__get_required_keywords(target_id, parent_id, grand_id)[-3:-1]
        cache_database.delete_cache(keywords, cache=cache)
        return self.crud.update_item(db, schema, target_id)

    def delete(
            self,
            db: Session,
            cache: Redis,
            target_id: UUID | None = None,
            parent_id: UUID | None = None,
            grand_id: UUID | None = None,
    ) -> Menu | SubMenu | Dish | None:
        keywords = self.__get_required_keywords(target_id, parent_id, grand_id)
        cache_database.delete_cache(keywords, cache=cache)
        return self.crud.delete_item(db, target_id)

    def __get_required_keywords(
            self,
            target_id: UUID | None = None,
            parent_id: UUID | None = None,
            grand_id: UUID | None = None
    ) -> list[str]:
        if target_id is None:
            menu_id, submenu_id, dish_id = None, None, None
        elif parent_id is None:
            menu_id, submenu_id, dish_id = target_id, None, None
        elif grand_id is None:
            menu_id, submenu_id, dish_id = parent_id, target_id, None
        else:
            menu_id, submenu_id, dish_id = grand_id, parent_id, target_id

        result = []
        match self.crud:
            case MenuCRUD():
                result = menu_keywords
            case SubMenuCRUD():
                result = menu_keywords[:-1] + submenu_keywords
            case DishCRUD():
                result = menu_keywords[:-1] + submenu_keywords[:-1] + dish_keywords
        return [keyword.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id) for keyword in result]
