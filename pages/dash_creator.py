from typing import Tuple, Optional
from io import BytesIO

from nicegui import ui, APIRouter, app
from nicegui.events import UploadEventArguments

from modules.components import top_bar, creator_tabs, content, thumb, thumb_panel
from modules.controllers import create_blog, create_course, fetch_owned_posts
from modules.helpers import load_class_name
from modules.models import User

# from modules.helpers import load_css

dash_router = APIRouter()


def write_a_blog(handle_click: callable):
    with ui.element("div"):
        with ui.element("div"):
            with ui.row().style("align-items: center; justify-content: center;"):
                ui.label("Title: ").style("text-justify: center;padding-bottom: 1em;")
                title = ui.input("Type a title for your blog here").style(
                    "width: 80%; padding-bottom: 1em;"
                )

            editor = ui.editor(placeholder="Type something here").style(
                "margin-bottom: 3em; height: 60vh; width: 100%"
            )

            ui.button("Save", on_click=lambda: handle_click(title, editor))


def create_a_course(handle_click: callable):
    file: Optional[Tuple[BytesIO, str]] = None

    def handle_upload(e: UploadEventArguments, upload):
        nonlocal file

        if not e.type.startswith("video"):
            ui.notify("Only videos are allowed", color="negative")
            upload.reset()
            return

        file = (e.content, e.name.split(".")[-1])

    with ui.element("div").style(
        "display: flex;"
        "flex-direction: row;"
        "justify-content: space-evenly;"
        "gap: 2em;"
        "width: 100%;"
    ):
        with ui.element("div").style("width: 45%"):
            ui.label("Title:").style("text-justify: center;padding-bottom: 1em;")
            title = ui.input("Type a title for your course here").style(
                "width: 80%; padding-bottom: 1em;"
            )
            ui.label("Description:").style("text-justify: center;padding-bottom: 1em;")
            description = ui.textarea("Type a description for your blog here")

            ui.button(
                "Save", on_click=lambda: handle_click(title, description, file, upload)
            ).style("margin-top: 2em")

        upload_class_name = load_class_name(
            """
            content: "Drag a video to upload, or click + ";
            display: block;
            position: absolute;
            top: 40%;
            font-size: 1.5em;
            width: 100%;
            padding: 0 1em;
            text-align: center;
        """,
            "::before",
        )

        upload = (
            ui.upload(
                auto_upload=True,
                multiple=False,
                max_files=1,
                on_upload=lambda e: handle_upload(e, upload),
            )
            .classes(upload_class_name)
            .style("position: relative;")
        )


@ui.refreshable
def publishing():
    posts = fetch_owned_posts()
    with thumb_panel():
        for post in posts:
            thumb(post)


@dash_router.page("/dash-creator")
def dashboard():
    user = User.get_user()

    top_bar(user)

    with content():
        with ui.row():
            write_a_blog_tab, create_a_course_tab, publishing_tab = creator_tabs()

            with publishing_tab:
                publishing()

            with write_a_blog_tab:

                def handle_create_blog(title, editor):
                    create_blog(title.value, editor.value)
                    for element in [title, editor]:
                        element.value = ""
                    publishing.refresh()

                write_a_blog(handle_create_blog)

            with create_a_course_tab.style("width: 100%"):

                def handle_create_course(title, description, file, upload):
                    if not title.value or not description.value or not file:
                        return ui.notify("Please fill all the fields", color="negative")

                    create_course(title.value, description.value, file)

                    upload.reset()
                    for element in [title, description]:
                        element.value = ""

                    publishing.refresh()

                create_a_course(handle_create_course)
