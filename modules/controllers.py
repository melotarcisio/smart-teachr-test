from typing import Dict
from nicegui import ui, app
from modules.models import User, Role


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
