"""
Глобальные настройки
"""
__author__ = '6dba'
__date__ = '28/04/2024'

from typing import Optional
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

    FTP_HOST:  Optional[str] = None
    FTP_USER: Optional[str] = None
    FTP_PASSWORD: Optional[str] = None

    SMB_HOST: Optional[str] = None
    SMB_SERVER_NAME: Optional[str] = None
    SMB_SHARE_NAME: Optional[str] = None
    SMB_USERNAME: Optional[str] = None
    SMB_PASSWORD: Optional[str] = None

    class Config:
        env_file = find_dotenv(".env")


settings = Settings()
