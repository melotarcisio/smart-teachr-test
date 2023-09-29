from typing import Union
from nicegui import ui, app
from modules.models import User, Posts, BlogWithUsername, CourseWithUsername
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


text_overflow = (
    "white-space: nowrap;"
    "overflow: hidden;"
    "text-overflow: ellipsis;"
    "inline-size: 90%"
)


def thumb(post: Posts):
    icon = "description" if isinstance(post, BlogWithUsername) else "videocam"
    with ui.card().style(
        "width: 23%; height: 6em; margin-bottom: 2em; position: relative"
    ).classes("bg-gray-100"):
        with ui.element("div").style(
            "display: flex; align-items: center; gap: 1em; width: 100%"
        ):
            ui.icon(icon).style("scale: 3;")
            with ui.element("div").style(
                "display: flex; flex-direction: column; justify-content: space-evenly; width: 100%"
            ):
                ui.label(post.title).style(f"font-size: 1.5rem;{text_overflow}")
                ui.label(f"Created by {post.username}").style(
                    f"font-size: 0.8rem; {text_overflow}"
                )

        ui.button(
            "",
            on_click=lambda: ui.notify("clicked"),
        ).style(
            "position: absolute;"
            "top: 0;"
            "right: 0;"
            "left: 0;"
            "right: 0;"
            "bottom: 0;"
            "opacity: 0;",
        )


def thumb_panel():
    return ui.element("div").style(
        "width: 100%;"
        "height: 100%;"
        "display: flex;"
        "flex-direction: row;"
        "flex-wrap: wrap;"
        "gap: 2%"
    )
