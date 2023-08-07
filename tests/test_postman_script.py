import pytest
from fastapi import status
from httpx import AsyncClient

from factories import DishFactory, MenuFactory


@pytest.mark.anyio
async def test_dishes_and_submenus_count(
    client: AsyncClient,
    two_dishes: tuple[DishFactory, DishFactory, MenuFactory],
):
    first_dish, second_dish, menu = two_dishes
    response = await client.get(
        f'/api/v1/menus/{menu.id}',
    )  # просматриваем конкретное меню
    assert response.json() == {
        'id': '2e1ce371-cd16-4231-bc5e-4fac25e314f2',
        'title': 'Dessert Features',
        'description': 'Menu of cakes, pastries and other sweet things',
        'submenus_count': 1,
        'dishes_count': 2,
    }
    assert response.status_code == status.HTTP_200_OK
    response = await client.get(
        f'/api/v1/menus/{menu.id}/submenus/{first_dish.submenu_id}',
    )  # просматриваем конкретное подменю
    assert response.json() == {
        'id': '86139c28-ceac-40f1-a71f-0f2c40a6290a',
        'title': 'Cakes',
        'description': 'Cakes from all sorrows',
        'dishes_count': 2,
    }
    assert response.status_code == status.HTTP_200_OK
    response = await client.delete(
        f'/api/v1/menus/{menu.id}/submenus/{first_dish.submenu_id}',
    )  # удаляем подменю
    assert response.json() == {
        'message': 'The submenu successfully deleted',
        'status': True,
    }
    assert response.status_code == status.HTTP_200_OK
    response = await client.get(
        f'/api/v1/menus/{menu.id}/submenus/',
    )  # просматриваем список подменю
    assert response.json() == []
    assert response.status_code == status.HTTP_200_OK
    response = await client.get(
        f'/api/v1/menus/{menu.id}/submenus/{second_dish.submenu_id}/dishes/',
    )  # просматриваем список блюд
    assert response.json() == []
    assert response.status_code == status.HTTP_200_OK
    response = await client.get(
        f'/api/v1/menus/{menu.id}',
    )  # просматриваем определенное меню
    assert response.json() == {
        'id': str(menu.id),
        'title': menu.title,
        'description': menu.description,
        'submenus_count': 0,
        'dishes_count': 0,
    }
    assert response.status_code == status.HTTP_200_OK
    response = await client.delete(f'/api/v1/menus/{menu.id}')  # удаляем меню
    assert response.json() == {
        'message': 'The menu successfully deleted',
        'status': True,
    }
    assert response.status_code == status.HTTP_200_OK
    response = await client.get('/api/v1/menus/')  # просматриваем список меню
    assert response.json() == []
    assert response.status_code == status.HTTP_200_OK
