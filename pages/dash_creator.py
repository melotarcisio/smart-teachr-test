from nicegui import ui, APIRouter, app

from modules.components import top_bar, creator_tabs, content, blog_thumb
from modules.controllers import create_blog
from modules.models import User, BlogWithUsername

# from modules.helpers import load_css

dash_router = APIRouter()


def write_a_blog(handle_click: callable):
    with ui.element("div"):
        with ui.element("div"):
            with ui.row():
                ui.label("Title: ")
                title = ui.input("Type a title for your blog here")

            editor = ui.editor(placeholder="Type something here").style(
                "margin-bottom: 3em; height: 60vh; width: 56vw"
            )

            ui.button("Save", on_click=lambda: handle_click(title, editor))


def create_a_course():
    ui.label("create")


def publishing(blogs: BlogWithUsername):
    with ui.element("div") as publish_component:
        for blog in blogs:
            blog_thumb(blog)

    return publish_component


dash_components = (write_a_blog, create_a_course, publishing)


@dash_router.page("/dash-creator")
def dashboard():
    user = User(**app.storage.user)
    blogs = BlogWithUsername.list_created()

    def handle_create_blog(title, editor):
        blog = create_blog(title.value, editor.value)
        for element in [title, editor]:
            element.value = ""
        blogs.append(blog.fill_username(user.username))
        ui.update(publish_component)

    top_bar(user)

    with content():
        with ui.row():
            write_a_blog_tab, create_a_course_tab, publishing_tab = creator_tabs()

            with write_a_blog_tab:
                write_a_blog(handle_create_blog)

            with create_a_course_tab:
                create_a_course()

            with publishing_tab:
                publish_component = publishing(blogs)
