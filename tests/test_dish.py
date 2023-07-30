from typing import Tuple

import pytest
from fastapi import status
from httpx import AsyncClient

from factories import DishFactory, MenuFactory, SubmenuFactory


@pytest.mark.anyio
async def test_dishes_list(
    client: AsyncClient,
    dish_and_menu: Tuple[DishFactory, MenuFactory],
):
    dish, menu = dish_and_menu
    response = await client.get(
        f"/api/v1/menus/{menu.id}/submenus/{dish.submenu_id}/dishes/",
    )
    assert response.json() == [
        {
            "id": str(dish.id),
            "title": dish.title,
            "description": dish.description,
            "price": "2.56",
        },
    ]
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_get_dish(
    client: AsyncClient,
    dish_and_menu: Tuple[DishFactory, MenuFactory],
):
    dish, menu = dish_and_menu
    response = await client.get(
        f"/api/v1/menus/{menu.id}/submenus/{dish.submenu_id}/dishes/{dish.id}",
    )

    current_dish = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert current_dish["id"] == str(dish.id)
    assert current_dish["title"] == dish.title
    assert current_dish["description"] == dish.description


@pytest.mark.anyio
async def test_create_dish(client: AsyncClient, submenu: SubmenuFactory):
    dish_data = {
        "title": "Test Dish",
        "description": "Test Description",
        "price": "9.99",
    }
    response = await client.post(
        f"/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}/dishes/",
        json=dish_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    created_dish = response.json()
    assert "id" in created_dish
    assert created_dish["title"] == dish_data["title"]
    assert created_dish["description"] == dish_data["description"]
    assert created_dish["price"] == dish_data["price"]


@pytest.mark.anyio
async def test_update_dish(
    client: AsyncClient,
    dish_and_menu: Tuple[DishFactory, MenuFactory],
):
    dish, menu = dish_and_menu
    update_data = {
        "title": "Updated dish",
        "description": "Updated description",
        "price": "1.99",
    }
    response = await client.patch(
        f"/api/v1/menus/{menu.id}/submenus/{dish.submenu_id}/dishes/{dish.id}",
        json=update_data,
    )
    assert response.json() == {
        "id": str(dish.id),
        "title": "Updated dish",
        "description": "Updated description",
        "price": "1.99",
    }
    assert response.status_code == status.HTTP_200_OK
    response_after_update = await client.get(
        f"/api/v1/menus/{menu.id}/submenus/{dish.submenu_id}/dishes/{dish.id}",
    )
    assert response_after_update.status_code == status.HTTP_200_OK
    assert update_data.items() <= response_after_update.json().items()


@pytest.mark.anyio
async def test_delete_dish(
    client: AsyncClient,
    dish_and_menu: Tuple[DishFactory, MenuFactory],
):
    dish, menu = dish_and_menu
    response = await client.delete(
        f"/api/v1/menus/{menu.id}/submenus/{dish.submenu_id}/dishes/{dish.id}",
    )
    assert response.json() is True
    assert response.status_code == status.HTTP_200_OK
    response_after_del = await client.get(
        f"/api/v1/menus/{menu.id}/submenus/{dish.submenu_id}/dishes/{dish.id}",
    )
    assert response_after_del.json() == {"detail": "dish not found"}
    assert response_after_del.status_code == status.HTTP_404_NOT_FOUND
    response_after_del_2 = await client.get(
        f"/api/v1/menus/{menu.id}/submenus/{dish.submenu_id}/dishes/",
    )
    assert response_after_del_2.json() == []
    assert response_after_del_2.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_delete_submenu_with_dish(
    client: AsyncClient,
    dish_and_menu: Tuple[DishFactory, MenuFactory],
):
    dish, menu = dish_and_menu
    response = await client.delete(
        f"/api/v1/menus/{menu.id}/submenus/{dish.submenu_id}",
    )
    assert response.json() is True
    assert response.status_code == status.HTTP_200_OK
    response_after_del = await client.get(
        f"/api/v1/menus/{menu.id}/submenus/{dish.submenu_id}/dishes/{dish.id}",
    )
    assert response_after_del.json() == {"detail": "dish not found"}
    assert response_after_del.status_code == status.HTTP_404_NOT_FOUND
    response_after_del_2 = await client.get(
        f"/api/v1/menus/{menu.id}/submenus/{dish.submenu_id}",
    )
    assert response_after_del_2.json() == {"detail": "submenu not found"}
    assert response_after_del_2.status_code == status.HTTP_404_NOT_FOUND
