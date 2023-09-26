from nicegui import APIRouter, ui
from pages.login import login_router

router = APIRouter()

router.include_router(login_router)
