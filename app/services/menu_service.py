from uuid import UUID

from app.repository.menu_repository import MenuRepository
from app.schemas.menu_schemas import MenuCreateUpdate
from app.services.cache_service import CacheService


class MenuService:
    def __init__(
        self,
        menu_repository: MenuRepository,
        cache: CacheService,
    ):
        self.menu_repository = menu_repository
        self.cache = cache

    async def get_all_menus(self):
        cached_menus = await self.cache.get('menu_list')
        if cached_menus:
            menus = cached_menus
        else:
            menus = await self.menu_repository.get_menus()
            await self.cache.set_list('menu_list', menus)
        return menus

    async def get_menu(self, menu_id: UUID):
        cached_menu = await self.cache.get(f'menu_{menu_id}')
        if cached_menu:
            db_menu = cached_menu
        else:
            db_menu = await self.menu_repository.get_menu_by_id(menu_id=menu_id)
        if not db_menu:
            return None
        await self.cache.set(f'menu_{menu_id}', db_menu)
        return db_menu

    async def create_menu(self, menu: MenuCreateUpdate):
        await self.cache.delete("menu_list")
        new_menu = await self.menu_repository.create_menu(menu=menu)
        return new_menu

    async def update_menu(self, menu_id: UUID, menu: MenuCreateUpdate):
        db_menu = await self.menu_repository.get_menu_by_id(menu_id=menu_id)
        if db_menu:
            upd_menu = await self.menu_repository.update_menu(
                menu_id=menu_id,
                menu=menu,
            )
            await self.cache.set(f'menu_{menu_id}', upd_menu)
            await self.cache.delete('menu_list')
            return upd_menu
        else:
            return None

    async def delete_menu(self, menu_id: UUID):
        db_menu = await self.menu_repository.get_menu_by_id(menu_id=menu_id)
        if db_menu:
            await self.menu_repository.delete_menu(menu_id=menu_id)
            await self.cache.delete_all()
            await self.cache.delete(f"menu_{menu_id}")
            await self.cache.delete("menu_list")
            return {'status': True, 'message': 'The menu successfully deleted'}
