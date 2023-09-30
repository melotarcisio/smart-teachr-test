import requests
from uuid import uuid4
import os
from typing import Tuple
from io import BytesIO
from core.settings import settings

if not settings.STORAGE_PATH.startswith("https://"):
    os.makedirs(settings.STORAGE_PATH, exist_ok=True)


def store_file(file: Tuple[BytesIO, str]):
    content, ext = file
    content.seek(0)

    url = f"{settings.STORAGE_PATH}{uuid4()}.{ext}"

    if url.startswith("https://"):
        requests.put(url, data=content.read())
    else:
        with open(url, "wb") as f:
            f.write(content.read())

    return url


def load_file(path: str):
    with open(path, "rb") as f:
        content = BytesIO(f.read())
    return content
