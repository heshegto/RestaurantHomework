from uuid import UUID
from app.databases.db.crud import DishCRUD, MenuCRUD, SubMenuCRUD


class CacheKeys:
    def __init__(self, db_crud_type: MenuCRUD | SubMenuCRUD | DishCRUD) -> None:
        menu_keys = [
            'menus',
            'menus:{menu_id}',
            'menus:{menu_id}:*',
        ]
        submenu_keys = [
            'menus:{menu_id}:submenus',
            'menus:{menu_id}:submenus:{submenu_id}',
            'menus:{menu_id}:submenus:{submenu_id}:*',
        ]
        dish_keys = [
            'menus:{menu_id}:submenus:{submenu_id}:dishes',
            'menus:{menu_id}:submenus:{submenu_id}:dishes:{dish_id}',
            'menus:{menu_id}:submenus:{submenu_id}:dishes:{dish_id}:*',
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
