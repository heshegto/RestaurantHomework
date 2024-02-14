from uuid import UUID

import openpyxl
from fastapi import Query
from fastapi.encoders import jsonable_encoder
from redis import Redis

from app.business.schemas import DishCreate, MenuCreate, SubMenuCreate
from app.databases.cache.cache import get_redis
from app.databases.cache.cache_invalidation import (
    invalidation_on_creation,
    invalidation_on_delete,
    invalidation_on_update,
)
from app.databases.db.crud import DishCRUD, MenuCRUD, SubMenuCRUD, read_everything
from app.databases.db.database import SessionLocal

file_path = 'app/admin/Menu.xlsx'


async def get_base_from_file() -> list[dict[str, list | str]]:
    base_from_file = []
    workbook = openpyxl.load_workbook(file_path)
    try:
        sheet = workbook.active
    finally:
        workbook.close()

    for row in sheet.iter_rows(values_only=True):
        item = {}
        if type(row[0]) is int:
            item['title'] = row[1]
            item['description'] = row[2]
            item['child_menu'] = []
            base_from_file.append(item)
        elif type(row[1]) is int:
            item['title'] = row[2]
            item['description'] = row[3]
            item['dish'] = []
            base_from_file[-1]['child_menu'].append(item)
        elif type(row[2]) is int:
            item['title'] = row[3]
            item['description'] = row[4]
            item['price'] = f'{round(float(row[5]), 2):.2f}'
            item['sale'] = row[6]
            base_from_file[-1]['child_menu'][-1]['dish'].append(item)
    return base_from_file


async def get_base_from_db() -> Query:
    async with SessionLocal() as session:
        return await read_everything(session)


def find_dict_by_key_value(list_of_dicts, key, value) -> dict[str, str] | None:
    for d in list_of_dicts:
        if d.get(key) == value:
            return d
    return None


class Updater:
    def __init__(
            self,
            data_from_db,
            data_from_file,
            target_id: UUID | None = None,
            parent_id: UUID | None = None,
            grand_id: UUID | None = None,
            red: Redis = get_redis(),
            crud_model: MenuCRUD | SubMenuCRUD | DishCRUD = MenuCRUD(),
            schema_model: type[MenuCreate] | type[SubMenuCreate] | type[DishCreate] = MenuCreate
    ) -> None:
        self.data_from_db = data_from_db
        self.data_from_file = data_from_file
        self.target_id = target_id
        self.parent_id = parent_id
        self.grand_id = grand_id
        self.red = red
        self.crud_model = crud_model
        self.schema_model = schema_model

    async def compare(self) -> None:
        for db_item in self.data_from_db:
            self.target_id = db_item['id']
            file_item = find_dict_by_key_value(self.data_from_file, 'title', db_item['title'])
            if not file_item:
                '''Check for excess data in database'''
                async with SessionLocal() as session:
                    await self.crud_model.delete_item(session, self.target_id)
                invalidation_on_delete(self.red, self.target_id, self.parent_id, self.grand_id)
            else:
                '''Check if data in database needs update'''
                flag = True
                for key in file_item.keys():
                    if db_item[key] != file_item[key]:
                        flag = False
                if not flag:
                    update_item = {i: file_item[i] for i in file_item.keys(
                    ) if i != 'child_menu' and i != 'dish' and i != 'sale'}
                    async with SessionLocal() as session:
                        await self.crud_model.update_item(
                            session,
                            self.schema_model.model_validate(update_item),
                            self.target_id
                        )
                    invalidation_on_update(self.red, self.target_id, self.parent_id, self.grand_id)
                    # if file_item['sale']:
                    #     cache_key = CacheKeys(self.crud_model)
                    #     keyword = cache_key.get_required_keys(self.target_id, self.parent_id, self.grand_id)[-2]+':sale'
                    #     cache_crud.create_cache(keyword, file_item['sale'], self.red)

                '''Start checking child items'''
                if 'child_menu' in db_item.keys():
                    submenu = Updater(
                        data_from_db=db_item['child_menu'],
                        data_from_file=file_item['child_menu'],
                        parent_id=self.target_id,
                        grand_id=self.parent_id,
                        crud_model=SubMenuCRUD(),
                        schema_model=SubMenuCreate
                    )
                    await submenu.compare()
                elif 'dish' in db_item.keys():
                    dish = Updater(
                        data_from_db=db_item['dish'],
                        data_from_file=file_item['dish'],
                        parent_id=self.target_id,
                        grand_id=self.parent_id,
                        crud_model=DishCRUD(),
                        schema_model=DishCreate
                    )
                    await dish.compare()

    async def push_new(self) -> None:
        for file_item in self.data_from_file:
            '''Pushing missing data to database'''
            db_item = find_dict_by_key_value(self.data_from_db, 'title', file_item['title'])
            if not db_item:
                create_item = {i: file_item[i] for i in file_item.keys() if i != 'child_menu' and i != 'dish'}
                async with SessionLocal() as session:
                    self.target_id = (await self.crud_model.create_item(
                        session,
                        self.schema_model.model_validate(create_item),
                        self.parent_id
                    )).id
                invalidation_on_creation(self.red, parent_id=self.parent_id, grand_id=self.grand_id)

                # if file_item['sale']:
                #     cache_key = CacheKeys(self.crud_model)
                #     keyword = cache_key.get_required_keys(self.target_id, self.parent_id, self.grand_id)[-2] + ':sale'
                #     cache_crud.create_cache(keyword, file_item['sale'], self.red)

                '''Checking child items for missing data'''
                if 'child_menu' in file_item.keys():
                    submenu = Updater(
                        data_from_db=[{}],
                        data_from_file=file_item['child_menu'],
                        parent_id=self.target_id,
                        grand_id=self.parent_id,
                        crud_model=SubMenuCRUD(),
                        schema_model=SubMenuCreate
                    )
                    await submenu.push_new()
                elif 'dish' in file_item.keys():
                    dish = Updater(
                        data_from_db=[{}],
                        data_from_file=file_item['dish'],
                        parent_id=self.target_id,
                        grand_id=self.parent_id,
                        crud_model=DishCRUD(),
                        schema_model=DishCreate
                    )
                    await dish.push_new()
            else:
                if 'child_menu' in file_item.keys():
                    submenu = Updater(
                        data_from_db=db_item['child_menu'],
                        data_from_file=file_item['child_menu'],
                        parent_id=self.target_id,
                        grand_id=self.parent_id,
                        crud_model=SubMenuCRUD(),
                        schema_model=SubMenuCreate
                    )
                    await submenu.push_new()
                elif 'dish' in file_item.keys():
                    dish = Updater(
                        data_from_db=db_item['dish'],
                        data_from_file=file_item['dish'],
                        parent_id=self.target_id,
                        grand_id=self.parent_id,
                        crud_model=DishCRUD(),
                        schema_model=DishCreate
                    )
                    await dish.push_new()


async def start() -> None:
    """
    if you start this function like this `asyncio.run(start())`, it will do it's job, but if start it from celery
    it will do nothing. I don't know how to solve it
    """
    data_from_db = jsonable_encoder(await get_base_from_db())
    data_from_file = await get_base_from_file()
    menu = Updater(data_from_db, data_from_file, crud_model=MenuCRUD(), schema_model=MenuCreate)
    await menu.compare()
    await menu.push_new()
