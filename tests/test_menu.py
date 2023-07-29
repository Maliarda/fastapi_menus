import pytest
from fastapi import status
from httpx import AsyncClient


from app.main import app
from factories import MenuFactory


@pytest.mark.anyio
async def test_menus_list(client: AsyncClient, menu: MenuFactory, ):

    response = await client.get("/api/v1/menus/")
    assert response.json() == [
        {
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description,
            "submenus_count": 0,
            "dishes_count": 0,
        }
    ]
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_create_menu(client: AsyncClient):
    menu_data = {"title": "Test Menu", "description": "Test Description"}
    url = app.url_path_for("create_menu")
    response = await client.post(
        url, json=menu_data, )
    assert response.status_code == status.HTTP_201_CREATED
    created_menu = response.json()
    assert "id" in created_menu
    assert created_menu["title"] == menu_data["title"]
    assert created_menu["description"] == menu_data["description"]


@pytest.mark.anyio
async def test_get_menu(client: AsyncClient, menu: MenuFactory, ):
    response = await client.get(f"/api/v1/menus/{menu.id}")
    current_menu = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert current_menu["id"] == str(menu.id)
    assert current_menu["title"] == menu.title
    assert current_menu["description"] == menu.description
    assert current_menu["submenus_count"] == 0
    assert current_menu["dishes_count"] == 0


@pytest.mark.anyio
async def test_delete_menu(client: AsyncClient, menu: MenuFactory, ):
    response = await client.delete(f"/api/v1/menus/{menu.id}")
    assert response.json() is True
    assert response.status_code == status.HTTP_200_OK
    response_after_del = await client.get(f"/api/v1/menus/{menu.id}")
    assert response_after_del.json() == {'detail': 'menu not found'}
    assert response_after_del.status_code == status.HTTP_404_NOT_FOUND
    response_after_del_2 = await client.get("/api/v1/menus/")
    assert response_after_del_2.json() == []
    assert response_after_del_2.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_update_menu(client: AsyncClient, menu: MenuFactory, ):
    update_data = {
        "title": "Updated menu",
        "description": "Updated description",
    }
    response = await client.patch(
        f"/api/v1/menus/{menu.id}",
        json=update_data,
    )
    assert response.json() == {
        "id": str(menu.id),
        "title": "Updated menu",
        "description": "Updated description",
        "submenus_count": 0,
        "dishes_count": 0,
    }
    assert response.status_code == status.HTTP_200_OK
    response_after_update = await client.get(f"/api/v1/menus/{menu.id}")
    assert response_after_update.status_code == status.HTTP_200_OK
    assert update_data.items() <= response_after_update.json().items()
