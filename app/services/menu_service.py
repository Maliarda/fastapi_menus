from uuid import UUID

from fastapi import Depends

from app.repository.menu_repository import MenuRepository
from app.schemas.menu_schemas import MenuCreateUpdate


class MenuService:
    def __init__(
        self,
        menu_repository: MenuRepository = Depends(MenuRepository),
    ):
        self.menu_repository = menu_repository

    async def get_all_menus(self):
        return await self.menu_repository.get_menus()

    async def get_menu(self, menu_id: UUID):
        db_menu = await self.menu_repository.get_menu_by_id(menu_id=menu_id)
        if not db_menu:
            return None
        return db_menu

    async def create_menu(self, menu: MenuCreateUpdate):
        return await self.menu_repository.create_menu(menu=menu)

    async def update_menu(self, menu_id: UUID, menu: MenuCreateUpdate):
        db_menu = await self.menu_repository.get_menu_by_id(menu_id=menu_id)
        if db_menu:
            return await self.menu_repository.update_menu(
                menu_id=menu_id,
                menu=menu,
            )
        else:
            return None

    async def delete_menu(self, menu_id: UUID):
        db_menu = await self.menu_repository.delete_menu(menu_id=menu_id)
        if db_menu is None:
            return None
        return {'status': True, 'message': 'The menu successfully deleted'}
