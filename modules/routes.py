from nicegui import APIRouter, ui
from pages.login import login_router
from pages.dashboard import dash_router

router = APIRouter()

router.include_router(login_router)
router.include_router(dash_router)
