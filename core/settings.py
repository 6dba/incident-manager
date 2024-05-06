"""
Глобальные настройки
"""
__author__ = '6dba'
__date__ = '28/04/2024'

from dotenv import find_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки проекта
    """
    RABBITMQ_DSN: str
    SIEM_NAME: str
    SIEM_PROVIDER: str
    SQL_DSN: str
    SQL_PATH: str
    SQL_DRIVER: str

    class Config:
        env_file = find_dotenv(".env.dev")


settings = Settings()
