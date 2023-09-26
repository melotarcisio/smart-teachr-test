from typing import Optional

from modules.models import User
from fastapi.responses import RedirectResponse

from nicegui import app, ui, APIRouter

login_router = APIRouter()


def try_login(username: str, password: str):
    try:
        user = User.from_db(username, password)
    except ValueError:
        ui.notify("Wrong username or password", color="negative")
        return

    if not user:
        ui.notify("User not found", color="negative")
        return

    app.storage.user.update(user.model_dump())
    ui.open(app.storage.user.get("referrer_path", "/dashboard"))


@login_router.page("/login")
def login() -> Optional[RedirectResponse]:
    if app.storage.user.get("authenticated", False):
        return RedirectResponse("/")

    with ui.card().classes("absolute-center"):
        username = ui.input("Username").on(
            "keydown.enter", lambda: try_login(username.value, password.value)
        )
        password = ui.input("Password", password=True, password_toggle_button=True).on(
            "keydown.enter", lambda: try_login(username.value, password.value)
        )
        ui.button("Log in", on_click=lambda: try_login(username.value, password.value))
