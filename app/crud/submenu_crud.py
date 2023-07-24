from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.submenu import Submenu
from app.schemas.submenu_schemas import SubmenuCreateUpdate


async def get_submenu_by_id(
    submenu_id: UUID,
    session: AsyncSession,
):
    submenu = await session.get(Submenu, submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenu


async def get_submenus_list(
    menu_id,
    session: AsyncSession,
):
    submenus_list = await session.execute(
        select(Submenu).where(Submenu.menu_id == menu_id),
    )
    return submenus_list.scalars().all()


async def create_new_submenu(
    menu_id: UUID,
    submenu: SubmenuCreateUpdate,
    session: AsyncSession,
):
    new_submenu = Submenu(title=submenu.title, description=submenu.description)
    new_submenu.menu_id = menu_id
    session.add(new_submenu)
    await session.commit()
    await session.refresh(new_submenu)
    return new_submenu


async def update_submenu_by_id(
    submenu_id: UUID,
    submenu: SubmenuCreateUpdate,
    session: AsyncSession,
):
    upd_submenu = await session.get(Submenu, submenu_id)
    upd_submenu_data = submenu.dict(exclude_unset=True)
    for k, v in upd_submenu_data.items():
        setattr(upd_submenu, k, v)
    await session.commit()
    await session.refresh(upd_submenu)
    return upd_submenu


async def delete_submenu_by_id(
    submenu_id: UUID,
    session: AsyncSession,
):
    del_submenu = await session.get(Submenu, submenu_id)
    if del_submenu:
        await session.delete(del_submenu)
        await session.commit()
        return True
    return False
