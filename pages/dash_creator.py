from nicegui import ui, APIRouter

from modules.components import top_bar

dash_router = APIRouter()


@dash_router.page("/dash-creator")
def dashboard():
    top_bar()

    ui.label("content")
