from typing import List
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306

    CORS_BACKEND_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://192.168.1.75:5000",
    ]

    class Config:
        env_file = "./.env"


settings = Settings()
