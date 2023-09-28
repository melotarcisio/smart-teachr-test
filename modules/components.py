from typing import Literal, List
from nicegui import ui, app
from modules.models import User, Role, BlogWithUsername
from modules.controllers import change_mode, change_to
from modules.helpers import load_css, primary_color, new_state


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


def content():
    ui.card().style(
        "position: absolute; top: 0; left: 0; bottom: 0; width: 20vw; overflow: auto; padding: 1em"
    ).classes("bg-gray-100")

    ui.card().style(
        "position: absolute; top: 0; left: 80vw; bottom: 0; width: 20vw"
    ).classes("bg-gray-100")

    return ui.card().style(
        "position: absolute; top: 0; left: 20vw; bottom: 0; width: 60vw; overflow-y: auto; padding-top: 1em"
    )


labels = ("Write a Blog", "Create a Course", "Publishing")


def creator_tabs():
    tab_elements = []

    with ui.tabs().classes("w-full") as tabs:
        for label in labels:
            tab_elements.append(ui.tab(label))

    with ui.tab_panels(tabs, value=tab_elements[0]).classes("w-full"):
        return tuple(ui.tab_panel(tab) for tab in tab_elements)


def blog_thumb(blog: BlogWithUsername):
    with ui.card().style("margin-bottom: 1em; padding: 0;"):
        with ui.row().style("width: 100%"):
            with ui.button().props("outline").classes("w-full").style("padding: 1em;"):
                ui.icon("description").style("margin-right: 1em;")
                ui.label(blog.title)
                ui.label(f"Created by {blog.username}").style("margin-left: auto")
