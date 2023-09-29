import re
from typing import Any, TypeVar, Tuple, Callable, List, Type

from nicegui import ui
from uuid import uuid4

primary_color = "rgb(88, 152, 212)"


def load_class_name(css: str, selector: str = ""):
    """
    Dynamically load a CSS style into the page HTML.
    Generates a random class name to avoid conflicts.
    """
    class_name = re.sub(r"[^a-zA-Z]", "", "loaded" + str(uuid4()))
    style_tag = "\n".join(
        [
            row.strip()
            for row in f"""
        <style>
            .{class_name}{selector} {{
                {css}
            }}
        </style>
        """.split(
                "\n"
            )
        ]
    )

    ui.add_head_html(style_tag)

    return class_name


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


T = TypeVar("T")


def new_state(initial_value: T) -> Tuple[T, Callable[[T], None]]:
    state = initial_value

    def set_state(new_value: Any):
        nonlocal state
        state = new_value

    return state, set_state
