from fastapi import HTTPException

from ..schemas import Dish, Menu, MenuRead, SubMenu, SubMenuRead


def is_dish_none(db_dish: Dish | list[dict[str, str | int]] | None) -> Dish | list[dict[str, str | int]]:
    if db_dish is None:
        raise HTTPException(
            status_code=404,
            detail='dish not found'
        )
    return db_dish


def is_submenu_none(
        db_submenu: SubMenu | SubMenuRead | list[dict[str, str | int]] | None
) -> SubMenu | SubMenuRead | list[dict[str, str | int]]:
    if db_submenu is None:
        raise HTTPException(
            status_code=404,
            detail='submenu not found'
        )
    return db_submenu


def is_menu_none(
        db_menu: Menu | MenuRead | list[dict[str, str | int]] | None
) -> Menu | MenuRead | list[dict[str, str | int]]:
    if db_menu is None:
        raise HTTPException(
            status_code=404,
            detail='menu not found'
        )
    return db_menu


all_responses = {
    'menu': {
        404: {
            'description': 'Menu not found',
            'content': {
                'application/json': {
                    'example': {'detail': 'menu not found'}
                }
            },
        },
        401: {
            'description': 'Menu creation error',
            'content': {
                'application/json': {
                    'example': {'detail': 'Menu creation error'}
                }
            },
        }
    },
    'submenu': {
        404: {
            'description': 'Submenu not found',
            'content': {
                'application/json': {
                    'example': {'detail': 'submenu not found'}
                }
            },
        },
        401: {
            'description': 'Submenu creation error',
            'content': {
                'application/json': {
                    'example': {'detail': 'Submenu creation error'}
                }
            },
        }
    },
    'dish': {
        404: {
            'description': 'Dish not found',
            'content': {
                'application/json': {
                    'example': {'detail': 'dish not found'}
                }
            },
        },
        401: {
            'description': 'Dish creation error',
            'content': {
                'application/json': {
                    'example': {'detail': 'Dish creation error'}
                }
            },
        }
    }
}
