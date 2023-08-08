from uuid import UUID

from pydantic import BaseModel


class Dish(BaseModel):
    """A Pydantic model representing a dish entity."""

    id: UUID
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': '3030',
                'title': 'Chicken soup',
                'description': 'it will get rid of all worries',
                'price': '2.99',
            },
        }


class DishCreateUpdate(BaseModel):
    """A Pydantic model representing the data for creating or updating a dish."""

    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Chicken soup',
                'description': "Soup like mom's",
                'price': '2.99',
            },
        }
