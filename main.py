from nicegui import app, ui

from core.auth import AuthMiddleware
from modules.routes import router
from core.settings import settings

app.add_middleware(AuthMiddleware)

app.include_router(router)


@ui.page("/")
def main_page() -> None:
    with ui.column().classes("absolute-center items-center"):
        ui.label(f'Hello {app.storage.user["username"]}!').classes("text-2xl")
        ui.button(
            on_click=lambda: (app.storage.user.clear(), ui.open("/login")),
            icon="logout",
        ).props("outline round")


ui.run(storage_secret=settings.SECRET)
