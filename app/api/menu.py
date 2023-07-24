from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.menu_crud import (
    create_new_menu,
    delete_menu_by_id,
    get_menu_by_id,
    get_menus_list,
    update_menu_by_id,
)
from app.schemas.menu_schemas import Menu, MenuCreateUpdate


router = APIRouter(tags=["Menu"], prefix="/api/v1/menus")


@router.get(
    "/",
    response_model=list[Menu],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_list_menus(
    session: AsyncSession = Depends(get_async_session),
):
    all_menus = await get_menus_list(session)
    return all_menus


@router.get(
    "/{menu_id}",
    response_model=Menu,
    status_code=status.HTTP_200_OK,
)
async def get_menu(
    menu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_menu_by_id(menu_id, session)


@router.post(
    "/",
    response_model=Menu,
    summary="Create a new menu",
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
    menu: MenuCreateUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create a Menu-record in database.
    Specify the title and the description to set."""
    return await create_new_menu(menu, session)


@router.patch(
    "/{menu_id}",
    response_model=Menu,
    status_code=status.HTTP_200_OK,
)
async def update_menu(
    menu_id: UUID,
    menu: MenuCreateUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Update a Menu-record in database.
    Specify the ID of the menu to be updated,
    it's new 'title' and 'description'."""
    return await update_menu_by_id(menu_id, menu, session)


@router.delete(
    "/{menu_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_menu(
    menu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_menu_by_id(menu_id, session)
