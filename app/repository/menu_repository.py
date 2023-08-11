from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.menu import Menu
from app.models.submenu import Submenu
from app.schemas.menu_schemas import MenuCreateUpdate


class MenuRepository:
    """A repository class for accessing menu data."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.model = Menu

    async def get_menu_by_id(self, menu_id: UUID) -> Menu:
        """Get menu by id"""
        return (
            await self.session.execute(
                select(self.model).where(self.model.id == menu_id),
            )
        ).scalar()

    async def get_menus(self) -> list[Menu]:
        """Get menus list."""
        return (
            (await self.session.execute(select(self.model)))
            .scalars()
            .fetchall()
        )

    async def create_menu(self, menu: MenuCreateUpdate):
        """Create a new menu."""
        new_menu = self.model(title=menu.title, description=menu.description)
        self.session.add(new_menu)
        await self.session.commit()
        await self.session.refresh(new_menu)
        return new_menu

    async def delete_menu(self, menu_id: UUID) -> None:
        """Delete menu item"""
        del_menu = await self.get_menu_by_id(menu_id=menu_id)
        await self.session.delete(del_menu)
        await self.session.commit()

    async def update_menu(self, menu_id: UUID, menu: MenuCreateUpdate) -> Menu:
        """Update menu item"""
        upd_menu = await self.get_menu_by_id(menu_id=menu_id)
        upd_menu_data = menu.dict(exclude_unset=True)
        for k, v in upd_menu_data.items():
            setattr(upd_menu, k, v)
        await self.session.commit()
        await self.session.refresh(upd_menu)
        return upd_menu

    async def get_menus_with_submenus_and_dishes(self):
        """Get menus list with submenus and dishes."""
        query = select(self.model).options(
            selectinload(Menu.submenu).selectinload(Submenu.dish),
        )
        result = await self.session.execute(query)
        menus = result.scalars().all()
        return menus
