from fastapi import FastAPI

from app.api.dish import router as dish_router
from app.api.menu import router as menu_router
from app.api.submenu import router as submenu_router
from app.core.config import settings


app = FastAPI(title=settings.app_title)

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
