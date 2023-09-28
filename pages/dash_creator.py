from nicegui import ui, APIRouter, app

from modules.components import top_bar, creator_tabs, content
from modules.models import User

dash_router = APIRouter()


def write_a_blog():
    ui.label("write")


def create_a_course():
    ui.label("create")


def publishing():
    ui.label("publishing")


dash_components = (write_a_blog, create_a_course, publishing)


@dash_router.page("/dash-creator")
def dashboard():
    user = User(**app.storage.user)

    top_bar(user)

    with content():
        with ui.row():
            tabs = creator_tabs()
            for i, tab in enumerate(tabs):
                with tab:
                    dash_components[i]()
