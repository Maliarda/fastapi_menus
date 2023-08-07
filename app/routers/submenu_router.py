from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_submenu_service
from app.schemas.submenu_schemas import Submenu, SubmenuCreateUpdate
from app.services.submenu_service import SubmenuService


router = APIRouter(
    tags=['Submenu'],
    prefix='/api/v1/menus/{menu_id}/submenus',
)


@router.get(
    '/',
    response_model=list[Submenu],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_list_submenus(
    menu_id: UUID,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.get_all_submenus(menu_id)


@router.get(
    '/{submenu_id}',
    response_model=Submenu,
    status_code=status.HTTP_200_OK,
)
async def get_submenu(
    submenu_id: UUID,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    submenu = await submenu_service.get_submenu(submenu_id)

    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found',
        )
    return submenu


@router.post(
    '/',
    response_model=Submenu,
    status_code=status.HTTP_201_CREATED,
)
async def create_submenu(
    menu_id: UUID,
    submenu: SubmenuCreateUpdate,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    new_submenu = await submenu_service.create_submenu(menu_id=menu_id, submenu=submenu)
    return new_submenu


@router.patch(
    '/{submenu_id}',
    response_model=Submenu,
    status_code=status.HTTP_200_OK,
)
async def update_submenu(
    submenu_id: UUID,
    submenu: SubmenuCreateUpdate,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    new_submenu = await submenu_service.update_submenu(submenu_id, submenu)
    return new_submenu


@router.delete(
    '/{submenu_id}',
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_service: SubmenuService = Depends(get_submenu_service),
):
    return await submenu_service.delete_submenu(submenu_id=submenu_id, menu_id=menu_id)
    # if not del_submenu:
    #     return None
    # return {'status': True, 'message': 'The submenu successfully deleted'}
    #
    # return await submenu_service.delete_submenu(
    #     menu_id=menu_id,
    #     submenu_id=submenu_id,
    # )
