from pydantic import BaseSettings
import os


class Config(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool
    REDIS_URL: str
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    class Config:
        env_file = f"{os.getcwd()}/.env"


CONFIG = Config()
