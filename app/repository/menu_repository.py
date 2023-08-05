from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.menu import Menu
from app.schemas.menu_schemas import MenuCreateUpdate


class MenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session
        self.model = Menu

    async def get_menu_by_id(self, menu_id: UUID):
        """Get menu by id"""
        return (
            await self.session.execute(
                select(self.model).where(self.model.id == menu_id),
            )
        ).scalar()

    async def get_menu_by_title(self, menu_title: str):
        """Get menu by title."""
        return (
            await self.session.execute(
                select(self.model).where(self.model.title == menu_title),
            )
        ).scalar()

    async def get_menus(self):
        """Get menus list."""
        return (await self.db.execute(select(self.model))).scalars().all()

    async def create_menu(self, menu: MenuCreateUpdate):
        """Create a new menu."""
        new_menu = self.model(**menu.dict())
        self.session.add(new_menu)
        await self.session.commit()
        return new_menu

    async def delete_menu(self, menu_id: UUID):
        """Delete menu item"""
        del_menu = await self.get_menu_by_id(menu_id=menu_id)
        if del_menu:
            await self.session.delete(del_menu)
            await self.session.commit()
            return True
        return False

    async def update_menu(self, menu_id: UUID):
        """Update menu item"""
        upd_menu = await self.get_menu_by_id(menu_id=menu_id)
        upd_menu_data = self.model.dict(exclude_unset=True)
        for k, v in upd_menu_data.items():
            setattr(upd_menu, k, v)
        await self.session.commit()
        await self.session.refresh(upd_menu)
        await self.session.commit()
        return upd_menu
