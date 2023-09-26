from nicegui import ui, APIRouter

from modules.components import top_bar

dash_router = APIRouter()


@dash_router.page("/dash-consumer")
def dashboard():
    top_bar()

    ui.label("content")
