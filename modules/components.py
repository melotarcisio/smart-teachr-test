from nicegui import ui


def asign(var, value):
    var = value


def top_bar():
    with ui.header(elevated=True).classes("items-center justify-end"):
        with ui.button(on_click=lambda: drawer.show()):
            ui.avatar("img:https://nicegui.io/logo_square.png", color="blue-2")

        with ui.drawer(side="right").style("flex-direction: column").classes(
            "flex items-end"
        ) as drawer:
            ui.label("Drawer content")
            ui.button("Close drawer", on_click=lambda: drawer.hide())
