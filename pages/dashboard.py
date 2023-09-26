from typing import Optional

from fastapi.responses import RedirectResponse

from nicegui import app, ui, APIRouter

from modules.components import top_bar

dash_router = APIRouter()


@dash_router.page("/dashboard")
def dashboard():
    top_bar()

    ui.label("content")
