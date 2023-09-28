from typing import ClassVar, Literal

from database import get_db
from pydantic import BaseModel
from core.auth import compare_passwords

from nicegui import app

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

    def update(self):
        data = self.model_dump()
        pk = data.pop(self.pk)
        db.update(self.table_name, data, {self.pk: pk})

    @classmethod
    def get(cls, key: str):
        result = db.select(cls.table_name, {cls.pk: key})
        assert len(result) == 1, "More than one result found"
        return cls(**result[0])


Role = Literal["creator", "consumer"]


class User(BaseModelDB):
    """Models a user."""

    table_name: ClassVar = "users"
    pk: ClassVar = "username"

    id: int
    username: str
    role: Role
    created_at: str

    @classmethod
    def from_username(cls, username: str, password: str = "", auth: bool = False):
        [result] = db.select(cls.table_name, {"username": username}) or [None]

        if not result:
            raise ValueError("User not found")

        db_password = result.pop("password")

        if auth:
            assert compare_passwords(password, db_password), "Wrong password"

        return cls(**result)

    @classmethod
    def get_user(cls):
        return cls.from_username(app.storage.user.get("username", ""))


class Blog(BaseModelDB):
    """Models a blog post."""

    table_name: ClassVar = "blogs"

    id: int = None
    user_id: int
    title: str
    content: str

    @classmethod
    def list_created(cls):
        user = User.get_user()
        return [cls(**blog) for blog in db.select(cls.table_name, {"user_id": user.id})]

    @classmethod
    def list_all(cls):
        return [cls(**blog) for blog in db.select(cls.table_name)]

    def fill_username(self, username: str) -> "BlogWithUsername":
        return BlogWithUsername(
            **self.model_dump(), username=username, table_name=self.table_name
        )


class BlogWithUsername(Blog):
    username: str

    @classmethod
    def list_all(cls):
        query_result = db.select_raw(
            """
            SELECT
                blogs.id as id,
                blogs.user_id as user_id,
                blogs.title as title,
                blogs.content as content,
                users.username as username
            FROM blogs
            INNER JOIN users ON users.id = blogs.user_id
        """
        )
        return [cls(**blog) for blog in query_result]

    @classmethod
    def list_created(cls):
        user = User.get_user()
        return [
            cls(**blog, username=user.username)
            for blog in db.select(cls.table_name, {"user_id": user.id})
        ]
