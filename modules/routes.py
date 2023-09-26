from nicegui import APIRouter
from pages.login import login_router
from pages.dash_creator import dash_router as dash_creator_router
from pages.dash_consumer import dash_router as dash_consumer_router

router = APIRouter()

router.include_router(login_router)
router.include_router(dash_creator_router)
router.include_router(dash_consumer_router)
