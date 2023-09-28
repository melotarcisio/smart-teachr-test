from nicegui import app, ui
from fastapi.responses import RedirectResponse

from core.auth import AuthMiddleware
from modules.routes import router
from core.settings import settings

app.add_middleware(AuthMiddleware)

app.include_router(router)


@ui.page("/")
def main_page() -> None:
    with ui.label("Loading..."):
        user_role = app.storage.user.get("role", "consumer")

        return RedirectResponse(f"/dash-{user_role}")


ui.run(storage_secret=settings.SECRET)
