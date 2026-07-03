from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Payment Service"

    database_url: str = (
        "sqlite+aiosqlite:///./payments.db"
    )

    class Config:
        env_file = ".env"


settings = Settings()