import os
import time
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    env_path: Path
    OAUTH_GOOGLE_CLIENT_SECRET: str
    OAUTH_GOOGLE_CLIENT_ID: str
    OAUTH_GITHUB_CLIENT_SECRET: str
    OAUTH_GITHUB_CLIENT_ID: str


    if os.getenv("DOCKER_ENV") == "true":
        os.environ["DB_HOST"] = "db"


    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Определяем путь к .env в родительской директории
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

    # Динамически выбираем конфигурацию
    if os.getenv("DOCKER_ENV") == "true":
        # В контейнере
        model_config = SettingsConfigDict(env_file=None)
    else:
        # В разработке
        model_config = SettingsConfigDict(env_file=env_path)

settings = Settings()