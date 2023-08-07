import pytest
from fastapi import status
from httpx import AsyncClient

from factories import MenuFactory, SubmenuFactory


@pytest.mark.anyio
async def test_submenus_list(client: AsyncClient, submenu: SubmenuFactory):
    response = await client.get(f'/api/v1/menus/{submenu.menu_id}/submenus/')
    assert response.json() == [
        {
            'id': str(submenu.id),
            'title': submenu.title,
            'description': submenu.description,
            'dishes_count': 0,
        },
    ]
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_get_submenu(client: AsyncClient, submenu: SubmenuFactory):
    response = await client.get(
        f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}',
    )

    current_submenu = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert current_submenu['id'] == str(submenu.id)
    assert current_submenu['title'] == submenu.title
    assert current_submenu['description'] == submenu.description
    assert current_submenu['dishes_count'] == 0


@pytest.mark.anyio
async def test_create_submenu(client: AsyncClient, menu: MenuFactory):
    submenu_data = {'title': 'Test Submenu', 'description': 'Test Description'}
    response = await client.post(
        f'/api/v1/menus/{menu.id}/submenus/',
        json=submenu_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    created_submenu = response.json()
    assert 'id' in created_submenu
    assert created_submenu['title'] == submenu_data['title']
    assert created_submenu['description'] == submenu_data['description']


@pytest.mark.anyio
async def test_update_submenu(
    client: AsyncClient,
    submenu: SubmenuFactory,
):
    update_data = {
        'title': 'Updated submenu',
        'description': 'Updated description',
    }
    response = await client.patch(
        f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}',
        json=update_data,
    )
    assert response.json() == {
        'id': str(submenu.id),
        'title': 'Updated submenu',
        'description': 'Updated description',
        'dishes_count': 0,
    }
    assert response.status_code == status.HTTP_200_OK
    response_after_update = await client.get(
        f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}',
    )
    assert response_after_update.status_code == status.HTTP_200_OK
    assert update_data.items() <= response_after_update.json().items()


@pytest.mark.anyio
async def test_delete_submenu(
    client: AsyncClient,
    submenu: SubmenuFactory,
):
    response = await client.delete(
        f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}',
    )
    assert response.json() == {
        'message': 'The submenu successfully deleted',
        'status': True,
    }
    assert response.status_code == status.HTTP_200_OK
    response_after_del = await client.get(
        f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}',
    )
    assert response_after_del.json() == {'detail': 'submenu not found'}
    assert response_after_del.status_code == status.HTTP_404_NOT_FOUND
    response_after_del_2 = await client.get(
        f'/api/v1/menus/{submenu.menu_id}/submenus/',
    )
    assert response_after_del_2.json() == []
    assert response_after_del_2.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_delete_menu_with_submenu(
    client: AsyncClient,
    submenu: SubmenuFactory,
):
    response = await client.delete(f'/api/v1/menus/{submenu.menu_id}')
    assert response.json() == {
        'message': 'The menu successfully deleted',
        'status': True,
    }
    assert response.status_code == status.HTTP_200_OK
    response_after_del = await client.get(
        f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}',
    )
    assert response_after_del.json() == {'detail': 'submenu not found'}
    assert response_after_del.status_code == status.HTTP_404_NOT_FOUND
    response_after_del_2 = await client.get(f'/api/v1/menus/{submenu.menu_id}')
    assert response_after_del_2.json() == {'detail': 'menu not found'}
    assert response_after_del_2.status_code == status.HTTP_404_NOT_FOUND
