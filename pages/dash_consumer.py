from nicegui import ui, APIRouter, app

from modules.components import top_bar
from modules.models import User

dash_router = APIRouter()


@dash_router.page("/dash-consumer")
def dashboard():
    user = User.get_user()

    top_bar(user)
