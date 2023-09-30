from typing import Union
from nicegui import ui, app
from modules.models import User, Post, BlogWithUsername, CourseWithUsername, Action
from modules.controllers import change_mode, change_to
from modules.helpers import (
    load_css,
    primary_color,
    load_class_name,
    get_many_time_ago,
)


def content(class_name: str = ""):
    load_css(
        """
    .nicegui-content {
        padding: 0;
        height: calc(100vh - 6em);
    }
        
    .page-container {
        background-color: white;
        height: 100%;
        overflow-x: hidden;
        overflow-y: auto;
    }

    @media (min-width: 1600px) { 
        .page-container {
            width: 60vw; 
            margin-left: 20vw; 
        }
    }

    """
    )

    with ui.element("div").classes("bg-gray-100 h-full w-full"):
        return ui.element("div").classes(f"page-container {class_name}")


labels = ("Write a Blog", "Create a Course", "Publishing")


def creator_tabs():
    tab_elements = []

    with ui.tabs().classes("w-full") as tabs:
        for label in labels:
            tab_elements.append(ui.tab(label))

    with ui.tab_panels(tabs, value=tab_elements[0]).classes("w-full"):
        return tuple(ui.tab_panel(tab) for tab in tab_elements)


def blog_view(blog: BlogWithUsername):
    editor_class_name = load_class_name(
        """
    pointer-events: none;
    height: 100%;
    border: unset;
    """
    )
    load_css(
        f"""
    .{editor_class_name} > div:first-child {{
        display: none;
    }}
    """
    )
    ui.editor(value=blog.content).classes(editor_class_name)


def course_view(course: CourseWithUsername):
    ui.video(course.url).style("width: 100%; height: 100%")
    ui.label(course.description).style("font-size: 0.8rem").style("margin-top: 1em")


text_overflow = (
    "white-space: nowrap;"
    "overflow: hidden;"
    "text-overflow: ellipsis;"
    "max-inline-size: 30vw"
)


def load_show_modal_css():
    load_css(
        f"""
        .dialog-class > div > div {{
            max-width: 60vw;
            max-height: 60vh;
        }}
        
        .post-header-font {{
            place-self: flex-end;
            {text_overflow}
        }}
        
        .post-content {{
            width: 100%;
            padding: 0.5em 1em;
            height: 80%;
        }}
        
        @media (max-width: 1024px) {{
            .dialog-class > div > div {{
                max-width: 100vw;
            }}
        }}
        """,
    )


def show_post(post: Post):
    with ui.dialog().classes("dialog-class") as dialog, ui.card().style(
        "width: 100%; height: 100%;"
    ):
        with ui.row().style("width: 100%;").style("border-bottom: 0.7px solid grey;"):
            with ui.row():
                ui.label(post.title).style("font-size: 2rem").classes(
                    "post-header-font"
                )
                ui.label(f"Created by {post.username}").style(
                    "font-size: 1rem"
                ).classes("post-header-font")

            ui.button(icon="close", on_click=dialog.close).style(
                "margin-left: auto"
            ).props("round outline")

        with ui.element("div").classes("post-content"):
            if isinstance(post, BlogWithUsername):
                blog_view(post)

            elif isinstance(post, CourseWithUsername):
                course_view(post)

    return dialog.open


def thumb(post: Post):
    icon = "description" if isinstance(post, BlogWithUsername) else "videocam"

    handle_show = show_post(post)

    thumb_class_name = load_class_name(
        """
        width: 23%; 
        height: 6em; 
        margin-bottom: 2em; 
        position: relative;
    """,
        include_css="""
            @media (max-width: 1024px) {
                .$CLASS_NAME {
                    width: 45%;
                }
            }
            @media (max-width: 768px) {
                .$CLASS_NAME {
                    width: 100%;
                }
            }
    """,
    )

    with ui.card().classes(f"bg-gray-100 {thumb_class_name}"):
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
            on_click=handle_show,
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
        "height: auto;"
        "display: flex;"
        "flex-direction: row;"
        "flex-wrap: wrap;"
        "gap: 2%"
    )


def get_action_label(action: Action, created_at: str):
    return {
        "see": f"Seen at {get_many_time_ago(created_at)}",
        "create": f"Created at {get_many_time_ago(created_at)}",
    }[action]


@ui.refreshable
def history():
    actions = Action.list_user_actions()

    for action in actions:
        icon = (
            "description" if isinstance(action.post, BlogWithUsername) else "videocam"
        )
        handle_show = show_post(action.post)

        with ui.card().style(
            "width: 100%; height: 6em; margin-bottom: 0.2em; position: relative; padding: 0 1em"
        ).classes("bg-gray-100"):
            with ui.element("div").style(
                "display: flex; align-items: center; gap: 1em; width: 100%; height: 100%"
            ):
                ui.icon(icon).style("scale: 3;")
                with ui.element("div").style(
                    "display: flex; flex-direction: column; justify-content: space-evenly; width: 100%"
                ):
                    ui.label(action.post.title).style(
                        f"font-size: 1.5rem;{text_overflow}"
                    )
                    ui.label(get_action_label(action.action, action.created_at)).style(
                        f"font-size: 0.8rem; {text_overflow}"
                    )

            ui.button(
                "",
                on_click=handle_show,
            ).style(
                "position: absolute;"
                "top: 0;"
                "right: 0;"
                "left: 0;"
                "right: 0;"
                "bottom: 0;"
                "opacity: 0;",
            )


@ui.refreshable
def top_bar(user: User):
    cursor_pointer = load_class_name(
        """
        cursor: pointer;
    """
    )

    with ui.header(elevated=True).classes("items-center w-full").style(
        "height: 6em; justify-content: space-between;"
    ):
        with ui.avatar(
            icon="manage_search",
        ).style(
            "scale: 1.5; position: relative;"
        ).classes(cursor_pointer):
            with ui.menu():
                with ui.element("div").style("width: auto;"):
                    history()

        with ui.avatar(icon="account_circle").style("scale: 1.3").classes(
            cursor_pointer
        ):
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
