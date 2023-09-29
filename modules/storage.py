from uuid import uuid4
import os
from typing import Tuple
from io import BytesIO
from core.settings import settings

os.makedirs(settings.STORAGE_PATH, exist_ok=True)


def store_file(file: Tuple[BytesIO, str]):
    content, ext = file
    local_path = os.path.join(settings.STORAGE_PATH, f"{uuid4()}.{ext}")
    with open(local_path, "wb") as f:
        content.seek(0)
        f.write(content.read())

    return local_path


def load_file(path: str):
    with open(path, "rb") as f:
        content = BytesIO(f.read())
    return content
