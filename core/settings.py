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
    MQ_DSN: str
    SIEM_NAME: str
    SIEM_PROVIDER: str
    SQL_DSN: str
    SQL_PATH: Optional[str] = None

    FTP_HOST:  str
    FTP_USER: Optional[str] = None
    FTP_PASSWORD: Optional[str] = None
    FTP_DIR_PATH: Optional[str] = None

    SMB_SHARE_NAME: Optional[str] = None
    SMB_HOST: Optional[str] = SMB_SHARE_NAME
    SMB_SHARE_DIR_PATH: Optional[str] = None
    SMB_USERNAME: Optional[str] = None
    SMB_PASSWORD: Optional[str] = None

    # Если в .env значение не задано - pydantic ругается на '' при инициализации, поэтому str or int,
    # после инициализации - кастуется
    COLLECTOR_POLLING_FREQ_SEC: Optional[str or int] = lambda val: int(val) if val else 60

    class Config:
        env_file = find_dotenv(".env")


settings = Settings()
