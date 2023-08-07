from uuid import UUID

from app.repository.submenu_repository import SubmenuRepository
from app.schemas.submenu_schemas import SubmenuCreateUpdate
from app.services.cache_service import CacheService


class SubmenuService:
    def __init__(
            self,
            submenu_repository: SubmenuRepository,
            cache: CacheService,
    ):
        self.submenu_repository = submenu_repository
        self.cache = cache

    async def get_all_submenus(self, menu_id: UUID):
        cached_submenus = await self.cache.get('submenu_list')
        if cached_submenus:
            submenus = cached_submenus
        else:
            submenus = await self.submenu_repository.get_submenus(menu_id=menu_id)
            await self.cache.set_list('submenu_list', submenus)
        return submenus

    async def get_submenu(self, submenu_id: UUID):
        cached_submenu = await self.cache.get(f'submenu_{submenu_id}')
        if cached_submenu:
            db_submenu = cached_submenu
        else:
            db_submenu = await self.submenu_repository.get_submenu_by_id(
                submenu_id=submenu_id,
            )
        if not db_submenu:
            return None
        await self.cache.set(f'submenu_{submenu_id}', db_submenu)
        return db_submenu

    async def create_submenu(
            self,
            menu_id: UUID,
            submenu: SubmenuCreateUpdate,
    ):
        new_submenu = await self.submenu_repository.create_submenu(
            submenu=submenu,
            menu_id=menu_id,
        )
        if new_submenu:
            await self.cache.delete(f'menu_{menu_id}')
            await self.cache.delete('submenu_list')
            await self.cache.delete('menu_list')
        return new_submenu

    async def update_submenu(
            self,
            submenu_id: UUID,
            submenu: SubmenuCreateUpdate,
    ):
        db_submenu = await self.submenu_repository.get_submenu_by_id(
            submenu_id=submenu_id,
        )
        if not db_submenu:
            return None
        upd_submenu = await self.submenu_repository.update_submenu(
            submenu_id=submenu_id,
            submenu=submenu,
        )
        await self.cache.set(f'submenu_{submenu_id}', upd_submenu)
        await self.cache.delete('submenu_list')
        return upd_submenu

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID):

        db_submenu = await self.submenu_repository.get_submenu_by_id(
            submenu_id=submenu_id,
        )
        if db_submenu:
            await self.submenu_repository.delete_submenu(submenu_id=submenu_id)
            await self.cache.delete(f'menu_{menu_id}')
            await self.cache.delete(f'submenu_{submenu_id}')
            await self.cache.delete('menu_list')
            await self.cache.delete('submenu_list')
            await self.cache.delete('dish_list')
            return {'status': True, 'message': 'The submenu successfully deleted'}
