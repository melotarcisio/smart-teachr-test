from typing import ClassVar, Literal

from database import get_db
from pydantic import BaseModel
from core.auth import compare_passwords

db = get_db()


class BaseModelDB(BaseModel):
    table_name: ClassVar = ""
    pk: str = "id"

    def model_dump(self, *, exclude=None, **_):
        to_exclude = set([*(exclude or []), "table_name"])
        model = super().model_dump(by_alias=True, exclude=to_exclude, exclude_none=True)
        return model

    def save(self):
        db.upsert(self.table_name, self.model_dump(exclude=["pk"]), [self.pk])

    @classmethod
    def get(cls, key: str):
        result = db.select(cls.table_name, {cls.pk: key})
        assert len(result) == 1, "More than one result found"
        return cls(**result[0])


class User(BaseModelDB):
    """Models a user."""

    table_name: ClassVar = "users"

    id: int
    username: str
    role: Literal["creator", "consumer"]
    created_at: str

    @classmethod
    def from_db(cls, username: str, password: str):
        [result] = db.select(cls.table_name, {"username": username}) or [None]

        if not result:
            raise ValueError("User not found")

        db_password = result.pop("password")

        assert compare_passwords(password, db_password), "Wrong password"

        return cls(**result)
