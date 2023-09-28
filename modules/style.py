from nicegui import ui
from uuid import uuid4

primary_color = "rgb(88, 152, 212)"


def load_css(css: str):
    class_name = f"{uuid4()}"

    style_tag = f"""
    <style>
        .{class_name} {{
            {css}
        }}
    </style>
    """.replace(
        "\n", ""
    )

    ui.html(style_tag)

    return class_name
