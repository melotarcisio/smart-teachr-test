from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
import hashlib
import hmac
import nicegui.globals
from nicegui import app
from core import settings

key = settings.SECRET.encode("utf-8")
unrestricted_page_routes = {"/login"}


def get_password_hash(password: str):
    return hmac.new(key, password.encode("utf-8"), hashlib.sha256).hexdigest()


def compare_passwords(password: str, hashed: str):
    return hashed == hmac.new(key, password.encode("utf-8"), hashlib.sha256).hexdigest()


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request, call_next):
        if not app.storage.user.get("authenticated", False):
            if (
                request.url.path in nicegui.globals.page_routes.values()
                and request.url.path not in unrestricted_page_routes
            ):
                app.storage.user[
                    "referrer_path"
                ] = request.url.path  # remember where the user wanted to go
                return RedirectResponse("/login")
        return await call_next(request)
