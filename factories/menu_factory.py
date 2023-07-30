import factory

from app.models.dish import Dish
from app.models.menu import Menu
from app.models.submenu import Submenu
from factories.utils import AsyncFactory


class MenuFactory(AsyncFactory):
    class Meta:
        model = Menu

    id = "2e1ce371-cd16-4231-bc5e-4fac25e314f2"
    title = "Dessert Features"
    description = "Menu of cakes, pastries and other sweet things"


class SubmenuFactory(AsyncFactory):
    class Meta:
        model = Submenu

    id = "86139c28-ceac-40f1-a71f-0f2c40a6290a"
    title = "Cakes"
    description = "Cakes from all sorrows"
    menu_id = factory.SubFactory(MenuFactory).get_factory().id


class DishFactory(AsyncFactory):
    class Meta:
        model = Dish

    id = "6fa89a0b-2ae0-4ab0-a39e-f2eaceab367f"
    title = "Red Velvet"
    description = "Devilish dessert"
    price = "2.56"
    submenu_id = factory.SubFactory(SubmenuFactory).get_factory().id
