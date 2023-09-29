from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    """Models the environment variables used around the application."""

    SECRET: str
    TEST_USER: str
    TEST_PASSWORD: str

    STORAGE_PATH: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_PORT: int = 5432

    class Config:
        """Configure the environment variable model to be case sensitive."""

        case_sensitive = True


settings = Settings()
