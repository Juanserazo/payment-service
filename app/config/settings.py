from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    app_name: str = "Payment Service"

    database_url: str = (
        "sqlite+aiosqlite:///./payments.db"
    )


settings = Settings()