from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Сервис меню"
    app_description: str = "Сервис меню"
    database_url: str
    postgres_url_test: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
