from nicegui import APIRouter, ui
from pages.login import login

router = APIRouter()


@router.page("/login")
def page():
    login()
