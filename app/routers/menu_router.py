from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_menu_service
from app.schemas.menu_schemas import Menu, MenuCreateUpdate
from app.services.menu_service import MenuService


router = APIRouter(tags=['Menu'], prefix='/api/v1/menus')


@router.get(
    '/',
    response_model=list[Menu],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_list_menus(
    menu_service: MenuService = Depends(get_menu_service),
) -> list[Menu] | list:
    """Get list of all menus."""
    menus_list = await menu_service.get_all_menus()
    return menus_list


@router.get(
    '/{menu_id}',
    response_model=Menu,
    status_code=status.HTTP_200_OK,
)
async def get_menu(
    menu_id: UUID,
    menu_service: MenuService = Depends(get_menu_service),
) -> Menu | None:
    """Get details of a specific menu."""
    menu = await menu_service.get_menu(menu_id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found',
        )

    return menu


@router.post(
    '/',
    response_model=Menu,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
    menu: MenuCreateUpdate,
    menu_service: MenuService = Depends(get_menu_service),
) -> Menu:
    """Create a new menu."""
    new_menu = await menu_service.create_menu(menu)
    return new_menu


@router.patch(
    '/{menu_id}',
    response_model=Menu,
    status_code=status.HTTP_200_OK,
)
async def update_menu(
    menu_id: UUID,
    menu: MenuCreateUpdate,
    menu_service: MenuService = Depends(get_menu_service),
):
    """Update details of an existing menu."""
    upd_menu = await menu_service.update_menu(menu_id, menu)
    return upd_menu


@router.delete(
    '/{menu_id}',
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_menu(
    menu_id: UUID,
    menu_service: MenuService = Depends(get_menu_service),
) -> dict | None:
    """Delete a menu."""
    del_menu = await menu_service.delete_menu(menu_id)
    if not del_menu:
        return None
    return {'status': True, 'message': 'The menu successfully deleted'}
