from pydantic import BaseSettings


class Settings(BaseSettings):
    """Models the environment variables used around the application."""

    TEST_USER: str
    TEST_PASSWORD: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_PORT: int = 5432

    class Config:
        """Configure the environment variable model to be case sensitive."""

        case_sensitive = True


settings = Settings()
