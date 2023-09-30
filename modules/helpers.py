from typing import List

from nicegui import ui
from hashlib import md5
from datetime import datetime

from modules.models import Post

primary_color = "rgb(88, 152, 212)"
full_size = "width: 100%; height: 100%;"
full_width = "width: 100%;"


def unique_class_name(css: str):
    return md5(css.encode("utf-8")).hexdigest()


def load_css(css: str):
    """
    Dynamically load a CSS style into the page HTML.
    """
    style_tag = "\n".join(
        [
            row.strip()
            for row in f"""
        <style>
            {css}
        </style>
        """.split(
                "\n"
            )
        ]
    )

    ui.add_head_html(style_tag)


def load_class_name(css: str, selector: str = "", include_css: str = ""):
    """
    Dynamically load a CSS style into the page HTML.
    Generates a random class name to avoid conflicts.
    """
    class_name = f"css-{unique_class_name(css)}"
    style_tag = "\n".join(
        [
            row.strip()
            for row in f"""
        <style>
            .{class_name}{selector} {{
                {css}
            }}
            {include_css.replace('$CLASS_NAME', class_name)}
        </style>
        """.split(
                "\n"
            )
        ]
    )

    ui.add_head_html(style_tag)

    return class_name


def leveshtein(str1: str, str2: str):
    if len(str1) > len(str2):
        str1, str2 = str2, str1

    distances = range(len(str1) + 1)
    for index2, char2 in enumerate(str2):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(str1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(
                    1
                    + min((distances[index1], distances[index1 + 1], new_distances[-1]))
                )
        distances = new_distances
    return distances[-1]


def filter_by_leveinshtein(posts: List[Post], filter_by: str):
    if len(filter_by) < 3:
        return posts

    post_distances = []

    for post in posts:
        distance = leveshtein(post.title, filter_by)
        if distance < 5 or post.title.lower().startswith(filter_by.lower()):
            post_distances.append((post, distance))

    return [post for post, _ in sorted(post_distances, key=lambda x: x[1])]


def get_many_time_ago(created_at: str):
    created_at_ = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    delta = now - created_at_

    if delta.days > 0:
        return f"{delta.days} days"

    if delta.seconds > 3600:
        return f"{delta.seconds // 3600} hours"

    if delta.seconds > 60:
        return f"{delta.seconds // 60} minutes"

    return f"{delta.seconds} seconds"
