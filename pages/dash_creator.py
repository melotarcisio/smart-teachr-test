from nicegui import ui, APIRouter, app

from modules.components import top_bar, creator_tabs, content, blog_thumb
from modules.controllers import create_blog
from modules.models import User, BlogWithUsername

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
                "margin-bottom: 3em; height: 60vh; width: 56vw"
            )

            ui.button("Save", on_click=lambda: handle_click(title, editor))


def create_a_course():
    ui.label("create")


@ui.refreshable
def publishing(blogs: BlogWithUsername):
    with ui.element("div") as publish_component:
        for blog in blogs:
            blog_thumb(blog)

    return publish_component


dash_components = (write_a_blog, create_a_course, publishing)


@dash_router.page("/dash-creator")
def dashboard():
    user = User(**app.storage.user)

    top_bar(user)

    with content():
        with ui.row():
            write_a_blog_tab, create_a_course_tab, publishing_tab = creator_tabs()

            with publishing_tab:
                publishing(BlogWithUsername.list_created())

            with write_a_blog_tab:

                def handle_create_blog(title, editor):
                    create_blog(title.value, editor.value)
                    for element in [title, editor]:
                        element.value = ""
                    publishing.refresh(BlogWithUsername.list_created())

                write_a_blog(handle_create_blog)

            with create_a_course_tab:
                create_a_course()
