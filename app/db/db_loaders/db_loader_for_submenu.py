from uuid import UUID

from redis import Redis
from sqlalchemy.orm import Session

from ...business import schemas
from .. import cache_database
from ..crud.crud_for_submenu import SubMenuCRUD


class SubmenuLoader:
    crud = SubMenuCRUD()

    def get_all_submenus(self, menu_id: UUID, db: Session, cache: Redis) -> list[dict]:
        keyword = f'menu:{str(menu_id)}:submenus'
        data = cache_database.read_cache(keyword, cache)
        if data:
            return data
        items = self.crud.read_all_items(menu_id, db).all()
        cache_database.create_cache(keyword, items, cache)
        return items

    def get_one_submenu(self, submenu_id: UUID, menu_id: UUID, db: Session, cache: Redis) -> list[dict] | None:
        keyword = f'menu:{str(menu_id)}:submenu:{str(submenu_id)}'
        data = cache_database.read_cache(keyword, cache)
        if data:
            return data
        items = self.crud.read_item_by_id(submenu_id, menu_id, db).first()
        cache_database.create_cache(keyword, items, cache)
        return items

    def create_submenu(
            self,
            menu_id: UUID,
            submenu: schemas.SubMenuCreate,
            db: Session,
            cache: Redis
    ) -> list[dict] | None:
        keywords = [
            'menus',
            f'menu:{str(menu_id)}',
            f'menu:{str(menu_id)}:submenus',
        ]
        cache_database.delete_cache(keywords, cache=cache)
        return self.crud.create_item(submenu, menu_id, db).first()

    def update_submenu(
            self,
            submenu_id: UUID,
            menu_id: UUID,
            submenu: schemas.SubMenuCreate,
            db: Session,
            cache: Redis
    ) -> list[dict] | None:
        keywords = [
            'menus',
            f'menu:{str(menu_id)}',
            f'menu:{str(menu_id)}:submenus',
            f'menu:{str(menu_id)}:submenu:{str(submenu_id)}',
        ]
        cache_database.delete_cache(keywords, cache=cache)
        return self.crud.update_item(submenu_id, submenu, db)

    def delete_submenu(self, submenu_id: UUID, menu_id: UUID, db: Session, cache: Redis) -> list[dict] | None:
        keywords = [
            'menus',
            f'menu:{str(menu_id)}',
            f'menu:{str(menu_id)}:submenus',
            f'menu:{str(menu_id)}:submenu:{str(submenu_id)}',
            f'menu:{str(menu_id)}:submenu:{str(submenu_id)}:*'
        ]
        cache_database.delete_cache(keywords, cache=cache)
        return self.crud.delete_item(submenu_id, db)
