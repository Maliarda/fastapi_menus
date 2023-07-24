from sqlalchemy import Column, String, func, select
from sqlalchemy.orm import MapperProperty, column_property, relationship

from app.core.db import Base
from app.models.submenu import Submenu


class Menu(Base):
    title = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    submenu = relationship(
        "Submenu",
        back_populates="menu",
        cascade="all, delete",
    )
    submenus_count: MapperProperty = column_property(
        select(func.count(Submenu.id))
        .where(Submenu.menu_id == id)
        .correlate_except(Submenu)
        .scalar_subquery(),
    )
