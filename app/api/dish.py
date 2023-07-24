from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.dish_crud import (
    create_new_dish,
    delete_dish_by_id,
    get_dish_by_id,
    get_dishes_list,
    update_dish_by_id,
)
from app.schemas.dish_schemas import Dish, DishCreateUpdate


router = APIRouter(
    tags=["Dish"],
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
)


@router.get(
    "/",
    response_model=list[Dish],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_list_dishes(
    submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    all_dishes = await get_dishes_list(submenu_id, session)
    return all_dishes


@router.get(
    "/{dish_id}",
    response_model=Dish,
    status_code=status.HTTP_200_OK,
)
async def get_dish(
    dish_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_dish_by_id(dish_id, session)


@router.post(
    "/",
    response_model=Dish,
    status_code=status.HTTP_201_CREATED,
)
async def create_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish: DishCreateUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    return await create_new_dish(menu_id, submenu_id, dish, session)


@router.patch(
    "/{dish_id}",
    response_model=Dish,
    status_code=status.HTTP_200_OK,
)
async def update_dish(
    dish_id: UUID,
    dish: DishCreateUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    return await update_dish_by_id(dish_id, dish, session)


@router.delete(
    "/{dish_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_submenu(
    dish_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_dish_by_id(dish_id, session)
