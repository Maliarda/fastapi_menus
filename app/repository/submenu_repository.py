from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.submenu import Submenu
from app.schemas.submenu_schemas import SubmenuCreateUpdate


class SubmenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session
        self.model = Submenu

    async def get_submenu_by_id(self, submenu_id: UUID) -> Submenu:
        """Get submenu by id."""
        return (
            await self.session.execute(
                select(self.model).where(self.model.id == submenu_id),
            )
        ).scalar()

    async def get_submenu_by_title(self, submenu_title: UUID):
        """Get submenu by title."""
        return (
            await self.session.execute(
                select(self.model).where(self.model.title == submenu_title),
            )
        ).scalar()

    async def get_submenus(self, menu_id: UUID):
        """Get submenus list."""
        return (
            (
                await self.session.execute(
                    select(self.model).where(self.model.menu_id == menu_id),
                )
            )
            .scalars()
            .all()
        )

    async def create_submenu(
        self,
        submenu: SubmenuCreateUpdate,
        menu_id: UUID,
    ):
        """Create a new submenu."""
        new_submenu = self.model(**submenu.dict())
        new_submenu.menu_id = menu_id
        self.session.add(new_submenu)
        await self.session.commit()
        await self.session.refresh(new_submenu)
        return new_submenu

    async def delete_submenu(self, submenu_id: UUID):
        """Delete submenu."""
        del_submenu = await self.get_submenu_by_id(submenu_id=submenu_id)
        if del_submenu:
            await self.session.delete(del_submenu)
            await self.session.commit()
            return True
        return False

    async def update_submenu(
        self,
        submenu_id: UUID,
        submenu: SubmenuCreateUpdate,
    ):
        """Update submenu."""
        upd_submenu = await self.get_submenu_by_id(submenu_id=submenu_id)
        upd_submenu_data = submenu.dict(exclude_unset=True)
        for k, v in upd_submenu_data.items():
            setattr(upd_submenu, k, v)
        await self.session.commit()
        await self.session.refresh(upd_submenu)
        return upd_submenu
