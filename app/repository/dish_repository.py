from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dish import Dish
from app.schemas.dish_schemas import DishCreateUpdate


class DishRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Dish

    async def get_dish_by_id(self, dish_id: UUID) -> Dish | None:
        """Get dish by id."""
        return (
            await self.session.execute(
                select(self.model).where(self.model.id == dish_id),
            )
        ).scalar()

    async def get_list_dishes(
            self, submenu_id: UUID,
    ) -> list[Dish] | None:
        """Get dishes list."""
        return (
            (
                await self.session.execute(
                    select(self.model)
                    .where(self.model.submenu_id == submenu_id)
                )
            )
            .scalars()
            .all()
        )

    async def create_dish(
            self,
            dish: DishCreateUpdate,
            menu_id: UUID,
            submenu_id: UUID,
    ) -> Dish:
        """Create a new dish."""
        new_dish = self.model(title=dish.title, description=dish.description, price=dish.price)
        new_dish.submenu_id = submenu_id
        self.session.add(new_dish)
        await self.session.commit()
        await self.session.refresh(new_dish)
        return new_dish

    async def delete_dish(self, dish_id: UUID) -> None:
        """Delete dish."""
        del_dish = await self.get_dish_by_id(dish_id=dish_id)
        await self.session.delete(del_dish)
        await self.session.commit()

    async def update_dish(self, dish_id: UUID, dish: DishCreateUpdate) -> Dish | None:
        """Update dish."""
        upd_dish = await self.get_dish_by_id(dish_id=dish_id)
        upd_dish_data = dish.dict(exclude_unset=True)
        for k, v in upd_dish_data.items():
            setattr(upd_dish, k, v)
        await self.session.commit()
        await self.session.refresh(upd_dish)
        return upd_dish
