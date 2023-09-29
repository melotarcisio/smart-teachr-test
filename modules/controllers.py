from typing import Dict, Tuple, List
from io import BytesIO

from nicegui import ui, app
from modules.models import (
    User,
    Role,
    Posts,
    Blog,
    Course,
    BlogWithUsername,
    CourseWithUsername,
)
from modules.storage import store_file

change_to: Dict[Role, Role] = {"creator": "consumer", "consumer": "creator"}
change_to_text = {key: f"{value.capitalize()} Mode" for key, value in change_to.items()}


def change_mode(user: User, change_to_role: Role):
    app.storage.user.update(
        {
            **app.storage.user,
            "role": change_to_role,
        }
    )
    user.role = change_to_role
    user.update()
    ui.open("/")


def create_blog(title: str, content: str):
    user = User.get_user()
    blog = Blog(title=title, content=content, user_id=user.id)
    blog.save()
    ui.notify("Blog created successfully", color="positive")
    return blog


def create_course(title: str, description: str, file: Tuple[BytesIO, str]):
    user = User.get_user()
    url = store_file(file)
    course = Course(title=title, description=description, url=url, user_id=user.id)
    course.save()
    ui.notify("Course created successfully", color="positive")
    return course


def fetch_owned_posts() -> List[Posts]:
    return sorted(
        [
            *BlogWithUsername.list_created(),
            *CourseWithUsername.list_created(),
        ],
        key=lambda x: x.created_at,
    )
