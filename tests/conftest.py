import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

import factories
from app.core.config import settings
from app.core.db import Base, get_async_session
from app.main import app


test_engine = create_async_engine(
    settings.postgres_url_test,
    future=True,
    echo=True,
    poolclass=NullPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


async def override_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True, scope="function")
async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    app.dependency_overrides = {get_async_session: override_db}
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def menu():
    menu = await factories.MenuFactory.create()
    yield menu


@pytest.fixture(scope="function")
async def submenu():
    menu = await factories.MenuFactory.create()
    submenu = await factories.SubmenuFactory.create(menu_id=menu.id)
    yield submenu


@pytest.fixture(scope="function")
async def dish_and_menu():
    menu = await factories.MenuFactory.create()
    submenu = await factories.SubmenuFactory.create(menu_id=menu.id)
    dish = await factories.DishFactory.create(submenu_id=submenu.id)
    yield dish, menu


@pytest.fixture(scope="function")
async def two_dishes():
    menu = await factories.MenuFactory.create()
    submenu = await factories.SubmenuFactory.create(menu_id=menu.id)
    first_dish = await factories.DishFactory.create(submenu_id=submenu.id)
    second_dish = await factories.DishFactory.create(
        submenu_id=submenu.id,
        id="2e1ce371-cd16-4231-bc5e-4fac25e314f2",
        title="Napoleon cake",
        description="Eat like an emperor",
        price="2.56",
    )
    yield first_dish, second_dish, menu
