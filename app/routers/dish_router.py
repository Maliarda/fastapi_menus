from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_dish_service
from app.schemas.dish_schemas import Dish, DishCreateUpdate
from app.services.dish_service import DishService


router = APIRouter(
    tags=['Dish'],
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
)


@router.get(
    '/',
    response_model=list[Dish],
    response_model_exclude_none=True,
    summary='Get lists of dishes',
    response_description='Dishes list',
    status_code=status.HTTP_200_OK,
)
async def get_list_dishes(
        submenu_id: UUID,
        dish_service: DishService = Depends(get_dish_service),
) -> list[Dish | None]:
    """Get list of all dishes."""
    return await dish_service.get_all_dishes(submenu_id=submenu_id)


@router.get(
    '/{dish_id}',
    response_model=Dish,
    status_code=status.HTTP_200_OK,
)
async def get_dish(
        dish_id: UUID,
        dish_service: DishService = Depends(get_dish_service),
) -> Dish | None:
    """Get details of a specific dish."""
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
) -> Dish:
    """Create a new dish."""
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
) -> Dish:
    """Update details of an existing dish."""
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
) -> dict | None:
    """Delete a dish."""

    dish = await dish_service.delete_dish(menu_id=menu_id,
                                          submenu_id=submenu_id,
                                          dish_id=dish_id)
    if dish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found',
        )
    return dish
