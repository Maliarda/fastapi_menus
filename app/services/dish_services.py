from uuid import UUID

from fastapi import Depends

from app.repository.dish_repository import DishRepository
from app.schemas.dish_schemas import DishCreateUpdate


class DishService:
    def __init__(
        self,
        dish_repository: DishRepository = Depends(DishRepository),
    ):
        self.dish_repository = dish_repository

    async def get_all_dishes(self, submenu_id: UUID):
        dishes = await self.dish_repository.get_list_dishes(
            submenu_id=submenu_id,
        )
        return dishes

    async def get_dish(self, dish_id: UUID):
        db_dish = await self.dish_repository.get_dish_by_id(dish_id=dish_id)
        if not db_dish:
            return None
        return db_dish

    async def create_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish: DishCreateUpdate,
    ):
        return await self.dish_repository.create_dish(
            dish=dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
        )

    async def update_dish(self, dish_id: UUID, dish: DishCreateUpdate):
        db_dish = await self.dish_repository.get_dish_by_id(dish_id=dish_id)
        if db_dish:
            return await self.dish_repository.update_dish(
                dish_id=dish_id,
                dish=dish,
            )
        else:
            return None

    async def delete_dish(self, dish_id: UUID):
        db_dish = await self.dish_repository.delete_dish(
            dish_id=dish_id
        )
        if db_dish is None:
            return None
        return {'status': True, 'message': 'The dish successfully deleted'}
