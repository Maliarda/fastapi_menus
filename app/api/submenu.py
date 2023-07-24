from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.submenu_crud import (
    create_new_submenu,
    delete_submenu_by_id,
    get_submenu_by_id,
    get_submenus_list,
    update_submenu_by_id,
)
from app.schemas.submenu_schemas import Submenu, SubmenuCreateUpdate


router = APIRouter(
    tags=["Submenu"],
    prefix="/api/v1/menus/{menu_id}/submenus",
)


@router.get(
    "/",
    response_model=list[Submenu],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_list_submenus(
    menu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    all_menus = await get_submenus_list(menu_id, session)
    return all_menus


@router.get(
    "/{submenu_id}",
    response_model=Submenu,
    status_code=status.HTTP_200_OK,
)
async def get_submenu(
    submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_submenu_by_id(submenu_id, session)


@router.post(
    "/",
    response_model=Submenu,
    status_code=status.HTTP_201_CREATED,
)
async def create_submenu(
    menu_id: UUID,
    submenu: SubmenuCreateUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    return await create_new_submenu(menu_id, submenu, session)


@router.patch(
    "/{submenu_id}",
    response_model=Submenu,
    status_code=status.HTTP_200_OK,
)
async def update_submenu(
    submenu_id: UUID,
    submenu: SubmenuCreateUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    return await update_submenu_by_id(submenu_id, submenu, session)


@router.delete(
    "/{submenu_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_submenu(
    submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_submenu_by_id(submenu_id, session)
