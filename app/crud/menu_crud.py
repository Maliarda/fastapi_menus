from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.menu import Menu
from app.schemas.menu_schemas import MenuCreateUpdate


async def get_menu_by_id(
    menu_id: UUID,
    session: AsyncSession,
):
    menu = await session.get(Menu, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


async def get_menus_list(
    session: AsyncSession,
):
    menus_list = await session.execute(select(Menu))
    return menus_list.scalars().all()


async def create_new_menu(
    menu: MenuCreateUpdate,
    session: AsyncSession,
):
    new_menu = Menu(title=menu.title, description=menu.description)
    session.add(new_menu)
    await session.commit()
    await session.refresh(new_menu)
    return new_menu


async def update_menu_by_id(
    menu_id: UUID,
    menu: MenuCreateUpdate,
    session: AsyncSession,
):
    upd_menu = await session.get(Menu, menu_id)
    upd_menu_data = menu.dict(exclude_unset=True)
    for k, v in upd_menu_data.items():
        setattr(upd_menu, k, v)
    await session.commit()
    await session.refresh(upd_menu)
    return upd_menu


async def delete_menu_by_id(
    menu_id: UUID,
    session: AsyncSession,
):
    del_menu = await session.get(Menu, menu_id)
    if del_menu:
        await session.delete(del_menu)
        await session.commit()
        return True
    return False
