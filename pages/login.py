from typing import Optional

from core.settings import settings
from modules.models import User
from fastapi.responses import RedirectResponse

from nicegui import app, ui, APIRouter

login_router = APIRouter()


def try_login(username: str, password: str):
    try:
        user = User.from_username(username, password, auth=True)
    except ValueError:
        ui.notify("Wrong username or password", color="negative")
        return

    if not user:
        ui.notify("User not found", color="negative")
        return

    app.storage.user.update(user.model_dump())
    ui.open(app.storage.user.get("referrer_path", f"/dash-{user.role}"))


@login_router.page("/login")
def login() -> Optional[RedirectResponse]:
    if app.storage.user.get("authenticated", False):
        return RedirectResponse("/")

    with ui.card().classes("absolute-center"):
        with ui.input("Username").on(
            "keydown.enter", lambda: try_login(username.value, password.value)
        ) as username:
            ui.tooltip("Test username: " + settings.TEST_USER).classes("right")

        with ui.input("Password", password=True, password_toggle_button=True).on(
            "keydown.enter", lambda: try_login(username.value, password.value)
        ) as password:
            ui.tooltip("Test password: " + settings.TEST_PASSWORD)

        ui.button("Log in", on_click=lambda: try_login(username.value, password.value))
