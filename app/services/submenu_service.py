from uuid import UUID

from fastapi import Depends

from app.repository.submenu_repository import SubmenuRepository
from app.schemas.submenu_schemas import SubmenuCreateUpdate


class SubmenuService:
    def __init__(
        self,
        submenu_repository: SubmenuRepository = Depends(SubmenuRepository),
    ):
        self.submenu_repository = submenu_repository

    async def get_all_submenus(self, menu_id: UUID):
        submenus = await self.submenu_repository.get_submenus(menu_id=menu_id)
        return submenus

    async def get_submenu(self, submenu_id: UUID):
        db_submenu = await self.submenu_repository.get_submenu_by_id(
            submenu_id=submenu_id,
        )
        if not db_submenu:
            return None
        return db_submenu

    async def create_submenu(
        self,
        menu_id: UUID,
        submenu: SubmenuCreateUpdate,
    ):
        return await self.submenu_repository.create_submenu(
            submenu=submenu,
            menu_id=menu_id,
        )

    async def update_submenu(
        self,
        submenu_id: UUID,
        submenu: SubmenuCreateUpdate,
    ):
        db_submenu = await self.submenu_repository.get_submenu_by_id(
            submenu_id=submenu_id,
        )
        if db_submenu:
            return await self.submenu_repository.update_submenu(
                submenu_id=submenu_id,
                submenu=submenu,
            )
        else:
            return None

    async def delete_submenu(self, submenu_id: UUID):
        db_submenu = await self.submenu_repository.delete_submenu(
            submenu_id=submenu_id,
        )
        if not db_submenu:
            return None
        return {'status': True, 'message': 'The submenu successfully deleted'}
