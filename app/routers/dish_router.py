from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.dish_schemas import Dish, DishCreateUpdate
from app.services.dish_service import DishService
from dependencies import get_dish_service


router = APIRouter(
    tags=['Dish'],
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
)


@router.get(
    '/',
    response_model=list[Dish],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_list_dishes(
        submenu_id: UUID,
        dish_service: DishService = Depends(get_dish_service),
):
    return await dish_service.get_all_dishes(submenu_id=submenu_id)


@router.get(
    '/{dish_id}',
    response_model=Dish,
    status_code=status.HTTP_200_OK,
)
async def get_dish(
        dish_id: UUID,
        dish_service: DishService = Depends(get_dish_service),
):
    dish = await dish_service.get_dish(dish_id=dish_id)

    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found',
        )
    return dish


@router.post(
    '/',
    response_model=Dish,
    status_code=status.HTTP_201_CREATED,
)
async def create_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish: DishCreateUpdate,
        dish_service: DishService = Depends(get_dish_service),
):
    new_dish = await dish_service.create_dish(menu_id, submenu_id, dish)
    return new_dish


@router.patch(
    '/{dish_id}',
    response_model=Dish,
    status_code=status.HTTP_200_OK,
)
async def update_dish(
        dish_id: UUID,
        dish: DishCreateUpdate,
        dish_service: DishService = Depends(get_dish_service),
):
    upd_dish = await dish_service.update_dish(dish_id, dish)
    return upd_dish


@router.delete(
    '/{dish_id}',
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish_service: DishService = Depends(get_dish_service),
):
    dish = await dish_service.delete_dish(menu_id=menu_id,
                                          submenu_id=submenu_id,
                                          dish_id=dish_id)
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found',
        )
    return dish
