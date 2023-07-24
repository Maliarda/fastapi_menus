from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.db import Base


class Dish(Base):
    title = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenu.id"))
    submenu = relationship(
        "Submenu",
        back_populates="dish",
    )
