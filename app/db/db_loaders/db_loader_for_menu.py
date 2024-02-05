from uuid import UUID

from redis import Redis
from sqlalchemy.orm import Session

from ...business import schemas
from .. import cache_database
from ..crud.crud_for_menu import MenuCRUD


class MenuLoader:
    crud = MenuCRUD()

    def get_all_menus(self, db: Session, cache: Redis):
        keyword = 'menus'
        data = cache_database.read_cache(keyword, cache)
        if data:
            return data
        items = self.crud.read_all_items(db).all()
        cache_database.create_cache(keyword, items, cache)
        return items

    def get_one_menu(self, menu_id: UUID, db: Session, cache: Redis):
        keyword = f'menu:{str(menu_id)}'
        data = cache_database.read_cache(keyword, cache)
        if data:
            return data
        items = self.crud.read_item_by_id(menu_id, db).first()
        cache_database.create_cache(keyword, items, cache)
        return items

    def create_menu(self, menu: schemas.MenuCreate, db: Session, cache: Redis):
        keyword = ['menus']
        cache_database.delete_cache(keyword, cache=cache)
        return self.crud.create_item(menu, db)

    def update_menu(self, menu_id: UUID, menu: schemas.MenuCreate, db: Session, cache: Redis):
        keywords = ['menus', f'menu:{str(menu_id)}']
        cache_database.delete_cache(keywords, cache=cache)
        return self.crud.update_item(menu_id, menu, db)

    def delete_menu(self, menu_id: UUID, db: Session, cache: Redis):
        keywords = ['menus', f'menu:{str(menu_id)}', f'menu:{str(menu_id)}:*']
        cache_database.delete_cache(keywords, cache=cache)
        return self.crud.delete_item(menu_id, db)
