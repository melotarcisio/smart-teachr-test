from typing import Any, TypeVar, Tuple, Callable, List, Type

from nicegui import ui
from uuid import uuid4

primary_color = "rgb(88, 152, 212)"


def load_css(css: str):
    class_name = str(uuid4())

    style_tag = "".join(
        [
            row.strip()
            for row in f"""
        <style>
            .{class_name} {{
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


T = TypeVar("T")


def new_state(initial_value: T) -> Tuple[T, Callable[[T], None]]:
    state = initial_value

    def set_state(new_value: Any):
        nonlocal state
        state = new_value

    return state, set_state
