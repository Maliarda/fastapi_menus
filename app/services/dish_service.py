from uuid import UUID

from app.repository.dish_repository import DishRepository
from app.schemas.dish_schemas import DishCreateUpdate
from app.services.cache_service import CacheService


class DishService:
    def __init__(
            self,
            dish_repository: DishRepository,
            cache: CacheService,
    ):
        self.dish_repository = dish_repository
        self.cache = cache

    async def get_all_dishes(self, submenu_id: UUID):
        cached_list = await self.cache.get('dish_list')
        if cached_list:
            dishes = cached_list
        else:
            dishes = await self.dish_repository.get_list_dishes(submenu_id=submenu_id)
            await self.cache.set_list('dish_list', dishes)
        return dishes

    async def get_dish(self, dish_id: UUID):
        cached_dish = await self.cache.get(f'dish_{dish_id}')
        if cached_dish:
            db_dish = cached_dish
        else:
            db_dish = await self.dish_repository.get_dish_by_id(dish_id=dish_id)
        if db_dish is None:
            return None
        await self.cache.set(f'dish_{dish_id}', db_dish)
        return db_dish

    async def create_dish(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish: DishCreateUpdate,
    ):
        await self.cache.delete_all()

        return await self.dish_repository.create_dish(dish=dish, menu_id=menu_id, submenu_id=submenu_id)

    async def update_dish(self, dish_id: UUID, dish: DishCreateUpdate):
        db_dish = await self.dish_repository.get_dish_by_id(dish_id=dish_id)
        if db_dish:
            upd_dish = await self.dish_repository.update_dish(
                dish_id=dish_id,
                dish=dish,
            )
            await self.cache.delete_all()
            return upd_dish

    async def delete_dish(self, dish_id: UUID, menu_id: UUID, submenu_id: UUID):
        db_dish = await self.dish_repository.get_dish_by_id(dish_id=dish_id)
        if db_dish is None:
            return None
        await self.dish_repository.delete_dish(dish_id=dish_id)
        await self.cache.delete_all()
        return {'status': 'true', 'message': 'The menu has been deleted'}
