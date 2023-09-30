from nicegui import ui, APIRouter, app

from modules.components import (
    top_bar,
    history,
    content,
    thumb_panel,
    blog_view,
    course_view,
    text_overflow,
    show_post,
    load_show_modal_css,
)
from modules.models import User, Post, BlogWithUsername, CourseWithUsername
from modules.controllers import fetch_all_posts, register_action
from modules.helpers import (
    filter_by_leveinshtein,
    full_width,
    load_class_name,
    get_many_time_ago,
)

dash_router = APIRouter()


def search_bar(on_change: callable):
    with ui.input("Search for a course or blog", on_change=on_change).style(
        "width: 30em; padding-bottom: 1em; margin: auto; position: relative"
    ).classes("search-bar bg-gray-100"):
        ui.icon(
            "search",
        ).style(
            "position: absolute; right: 1em; top: 70%; transform: translateY(-50%); scale: 1.5;"
        )


def post_wrapper(post: Post):
    def handle_show():
        start_show = show_post(post)
        start_show()
        register_action("see", post)
        history.refresh()

    post_class_name = load_class_name(
        """
        background-color: white;
        width: 100%;
        display: flex;
        flex-direction: column;
        padding: 1.8em;
        border-radius: 0.5em;
        margin-bottom: 1em;
        position: relative;
    """,
        include_css=f"""
    .$CLASS_NAME > div:first-child {{
        display: flex;
        justify-content: space-between;
        border-bottom: 0.7px solid grey;
        margin-bottom: 0.5em;
    }}
    .$CLASS_NAME > div:first-child > div:first-child {{
        {text_overflow};
        max-inline-size: 80%;
    }}
    .$CLASS_NAME > div:first-child > div:last-child {{
        align-items: self-end;
    }}
    .$CLASS_NAME > button {{
        opacity: 0;
        position: absolute;
        top: 0;
        bottom: 0;
        right: 0;
        left: 0;
    }}
    
    @media (max-width: 1024px) {{
        .$CLASS_NAME > div:first-child > div:first-child {{
            max-inline-size: 60%;
        }}
    }}
    """,
    )
    with ui.element("div").style(f"{full_width}").classes(post_class_name) as card:
        with ui.row().style(full_width):
            ui.label(post.title).style("font-size: 2rem").classes("post-header-font")
            with ui.column():
                ui.label(f"Created by {post.username}")
                ui.label(f"{get_many_time_ago(post.created_at)} ago")

        ui.button(on_click=handle_show)

        return card


@ui.refreshable
def publishing(all_posts: Post, filter_by: str = ""):
    posts_to_show = filter_by_leveinshtein(all_posts, filter_by)

    with thumb_panel():
        for post in posts_to_show:
            with post_wrapper(post):
                if isinstance(post, BlogWithUsername):
                    blog_view(post)
                elif isinstance(post, CourseWithUsername):
                    course_view(post)


@dash_router.page("/dash-consumer")
def dashboard():
    load_show_modal_css()
    user = User.get_user()
    all_posts = fetch_all_posts()

    filter_by = ""

    def handle_change_filter(input_):
        nonlocal filter_by, all_posts
        filter_by = input_.value
        publishing.refresh(all_posts, filter_by)

    top_bar(user)

    with content("bg-gray-100"):
        search_bar(handle_change_filter)
        publishing(all_posts, filter_by)
