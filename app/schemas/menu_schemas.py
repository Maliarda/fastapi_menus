from uuid import UUID

from pydantic import BaseModel


class Menu(BaseModel):
    id: UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "",
                "title": "Main menu",
                "description": "Main menu description",
                "submenus_count": 10,
                "dishes_count": 50,
            },
        }


class MenuCreateUpdate(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Main menu",
                "description": "Main menu description",
            },
        }
