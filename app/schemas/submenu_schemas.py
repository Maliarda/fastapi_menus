from uuid import UUID

from pydantic import BaseModel


class Submenu(BaseModel):
    id: UUID
    title: str
    description: str
    dishes_count: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "c1dd2867-1ed1-4839-a49b-de9cc9ac62b1 ",
                "title": "Cakes",
                "description": "Cakes description",
                "dishes_count": 20,
            },
        }


class SubmenuCreateUpdate(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Cakes",
                "description": "heavenly pleasure",
            },
        }
