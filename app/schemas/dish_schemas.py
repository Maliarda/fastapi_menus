from uuid import UUID

from pydantic import BaseModel


class Dish(BaseModel):
    id: UUID
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "3030",
                "title": "Chicken soup",
                "description": "it will get rid of all worries",
                "price": "2.99",
            },
        }


class DishCreateUpdate(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Chicken soup",
                "description": "Soup like mom's",
                "price": "2.99",
            },
        }
