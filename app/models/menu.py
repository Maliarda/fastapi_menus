import uuid

from sqlalchemy import Column, String, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import MapperProperty, column_property, relationship

from app.core.db import Base
from app.models.dish import Dish
from app.models.submenu import Submenu


class Menu(Base):
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        unique=True,
        default=uuid.uuid4,
    )
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
    dishes_count: MapperProperty = column_property(
        select(func.count(Dish.id))
        .join(Submenu, Submenu.menu_id == id)
        .where(Dish.submenu_id == Submenu.id)
        .correlate_except(Submenu)
        .scalar_subquery(),
    )
