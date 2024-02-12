from uuid import UUID
from app.databases.db.crud import DishCRUD, MenuCRUD, SubMenuCRUD


class CacheKeys:
    def __init__(self, db_crud_type: MenuCRUD | SubMenuCRUD | DishCRUD):
        menu_keys = [
            'menus',
            'menu:{menu_id}',
            'menu:{menu_id}:*',
        ]
        submenu_keys = [
            'menu:{menu_id}:submenus',
            'menu:{menu_id}:submenu:{submenu_id}',
            'menu:{menu_id}:submenu:{submenu_id}:*',
        ]
        dish_keys = [
            'menu:{menu_id}:submenu:{submenu_id}:dishes',
            'menu:{menu_id}:submenu:{submenu_id}:dish:{dish_id}',
            'menu:{menu_id}:submenu:{submenu_id}:dish:{dish_id}:*',
        ]
        match db_crud_type:
            case MenuCRUD():
                self.all_keys = menu_keys
            case SubMenuCRUD():
                self.all_keys = menu_keys[:-1] + submenu_keys
            case DishCRUD():
                self.all_keys = menu_keys[:-1] + submenu_keys[:-1] + dish_keys

    def get_required_keys(
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
        return [keyword.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id) for keyword in self.all_keys]
