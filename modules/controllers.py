from typing import Dict, Tuple, List
from io import BytesIO

from nicegui import ui, app
from modules.models import (
    User,
    Role,
    Post,
    Blog,
    Course,
    BlogWithUsername,
    CourseWithUsername,
    Action,
    ActionType,
)
from modules.storage import store_file


change_to: Dict[Role, Role] = {"creator": "consumer", "consumer": "creator"}
change_to_text = {key: f"{value.capitalize()} Mode" for key, value in change_to.items()}


def register_action(action: ActionType, post: Post):
    user = User.get_user()
    new_action = Action(
        action=action,
        reference_id=post.id,
        user_id=user.id,
        reference_table=post.table_name,
    )
    new_action.save()
    return new_action


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
    id_ = blog.save()
    blog.id = id_
    ui.notify("Blog created successfully", color="positive")
    register_action("create", blog)
    return blog


def create_course(title: str, description: str, file: Tuple[BytesIO, str]):
    user = User.get_user()
    url = store_file(file)
    course = Course(title=title, description=description, url=url, user_id=user.id)
    id_ = course.save()
    course.id = id_
    ui.notify("Course created successfully", color="positive")
    register_action("create", course)
    return course


def fetch_owned_posts() -> List[Post]:
    return sorted(
        [
            *BlogWithUsername.list_created(),
            *CourseWithUsername.list_created(),
        ],
        key=lambda x: x.created_at,
    )


def fetch_all_posts():
    return sorted(
        [
            *BlogWithUsername.list_all(),
            *CourseWithUsername.list_all(),
        ],
        key=lambda x: x.created_at,
    )


def list_user_actions():
    return Action.list_user_actions()
