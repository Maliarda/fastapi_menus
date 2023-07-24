from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dish import Dish
from app.schemas.dish_schemas import DishCreateUpdate


async def get_dish_by_id(
    dish_id: UUID,
    session: AsyncSession,
):
    dish = await session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


async def get_dishes_list(
    submenu_id: UUID,
    session: AsyncSession,
):
    dishes_list = await session.execute(
        select(Dish).where(Dish.submenu_id == submenu_id),
    )
    return dishes_list.scalars().all()


async def create_new_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish: DishCreateUpdate,
    session: AsyncSession,
):
    new_dish = Dish(
        title=dish.title,
        description=dish.description,
        price=dish.price,
    )
    new_dish.menu_id = menu_id
    new_dish.submenu_id = submenu_id
    session.add(new_dish)
    await session.commit()
    await session.refresh(new_dish)
    return new_dish


async def update_dish_by_id(
    dish_id: UUID,
    dish: DishCreateUpdate,
    session: AsyncSession,
):
    upd_dish = await session.get(Dish, dish_id)
    upd_dish_data = dish.dict(exclude_unset=True)
    for k, v in upd_dish_data.items():
        setattr(upd_dish, k, v)
    await session.commit()
    await session.refresh(upd_dish)
    return upd_dish


async def delete_dish_by_id(
    dish_id: UUID,
    session: AsyncSession,
):
    del_dish = await session.get(Dish, dish_id)
    if del_dish:
        await session.delete(del_dish)
        await session.commit()
        return True
    return False
