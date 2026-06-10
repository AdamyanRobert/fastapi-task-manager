from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    DATABASE_URL: str  # Railway подставит автоматически

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        url = self.DATABASE_URL
        # Railway может отдать postgres:// — заменяем
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)\
                  .replace("postgres://", "postgresql+asyncpg://", 1)

    @property
    def DATABASE_URL_psycopg(self) -> str:
        url = self.DATABASE_URL
        return url.replace("postgresql://", "postgresql+psycopg2://", 1)\
                  .replace("postgres://", "postgresql+psycopg2://", 1)

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

settings = Settings()

