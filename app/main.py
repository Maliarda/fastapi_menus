from fastapi import FastAPI

from app.core.config import settings
from app.core.redis import cache_init
from app.routers.dish_router import router as dish_router
from app.routers.menu_router import router as menu_router
from app.routers.submenu_router import router as submenu_router


app = FastAPI(title=settings.app_title)


@app.on_event('startup')
async def on_startup() -> None:
    await cache_init()

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
