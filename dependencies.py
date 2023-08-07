from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.redis import get_cache as get_redis
from app.repository.dish_repository import DishRepository
from app.repository.menu_repository import MenuRepository
from app.repository.submenu_repository import SubmenuRepository
from app.services.cache_service import CacheService
from app.services.dish_service import DishService
from app.services.menu_service import MenuService
from app.services.submenu_service import SubmenuService


def get_cache(cache=Depends(get_redis)):
    return CacheService(cache)


###
# MENU
###
def get_menu_repository(session: AsyncSession = Depends(get_async_session)):
    return MenuRepository(session)


def get_menu_service(
        repository: MenuRepository = Depends(get_menu_repository),
        cache: CacheService = Depends(get_cache),
):
    return MenuService(repository, cache)


###
# SUBMENU
###
def get_submenu_repository(session: AsyncSession = Depends(get_async_session)):
    return SubmenuRepository(session)


def get_submenu_service(
    repository: SubmenuRepository = Depends(get_submenu_repository),
    cache: CacheService = Depends(get_cache),
):
    return SubmenuService(repository, cache)


###
# DISHES
###
async def get_dish_repository(session: AsyncSession = Depends(get_async_session)):
    return DishRepository(session)


async def get_dish_service(
    repository: DishRepository = Depends(get_dish_repository),
    cache: CacheService = Depends(get_cache),
):
    return DishService(repository, cache=cache)
