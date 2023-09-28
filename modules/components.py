from nicegui import ui, app
from modules.models import User
from modules.controllers import change_mode, change_to_text, change_to
from modules.style import load_css


primary_color = "rgb(88, 152, 212)"


def top_bar(user: User):
    with ui.header(elevated=True).classes("items-center justify-end").style(
        "height: 6em"
    ):
        with ui.avatar(icon="account_circle").style("scale: 1.3"):
            with ui.menu().classes("column").style(
                "height: 15em, width: 7em; padding: 0.5em"
            ):
                ui.label(user.role).style("font-size: 1.5rem").classes(
                    "uppercase text-center"
                ).style(f"color: {primary_color}")
                ui.separator().style("margin: 1em 0")
                ui.button(
                    change_to[user.role],
                    on_click=lambda: change_mode(user, change_to[user.role]),
                    icon="change_circle",
                ).props("outline").props("no-wrap").style("margin-bottom: 1em")
                ui.button(
                    "Logout",
                    on_click=lambda: (app.storage.user.clear(), ui.open("/login")),
                    icon="logout",
                ).props("outline").props("space-between")
