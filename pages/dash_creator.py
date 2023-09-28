from nicegui import ui, APIRouter, app

from modules.components import top_bar
from modules.models import User

dash_router = APIRouter()


@dash_router.page("/dash-creator")
def dashboard():
    user = User(**app.storage.user)

    top_bar(user)

    ui.label("content")
