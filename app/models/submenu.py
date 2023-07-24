from sqlalchemy import Column, ForeignKey, String, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import MapperProperty, column_property, relationship

from app.core.db import Base
from app.models.dish import Dish


class Submenu(Base):
    title = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menu.id"))
    dishes_count: MapperProperty = column_property(
        select(func.count(Dish.id))
        .where(Dish.submenu_id == id)
        .correlate_except(Dish)
        .scalar_subquery(),
    )
    menu = relationship("Menu", back_populates="submenu")
    dish = relationship(
        "Dish",
        back_populates="submenu",
        cascade="all, delete",
    )
