from uuid import UUID

from pydantic import BaseModel


class Menu(BaseModel):
    """A Pydantic model representing a menu entity."""

    id: UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': '8da6b58f-8924-4cbb-9db6-64898f33d0d3',
                'title': 'Main menu',
                'description': 'Main menu description',
                'submenus_count': 10,
                'dishes_count': 50,
            },
        }


class MenuCreateUpdate(BaseModel):
    """A Pydantic model representing the data for creating or updating a menu."""

    title: str
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Main menu',
                'description': 'Main menu description',
            },
        }
