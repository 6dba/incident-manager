"""
Подключение к различным источникам данных
"""
__author__ = "6dba"
__date__ = "28/04/2024"

import asyncpg
from abc import ABC, abstractmethod

from core.settings import settings


class AbstractDatabaseConnection(ABC):
    @abstractmethod
    async def __aenter__(self): raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type): raise NotImplementedError


class PostgreSQLConnection(AbstractDatabaseConnection):
    """
    Асинхронного подключения к PostgreSQL
    """
    def __init__(self):
        self.__connection = None

    async def __aenter__(self):
        self.__connection = await asyncpg.connect(dsn=settings.SQL_DSN)
        return self.__connection

    async def __aexit__(self, *_):
        await self.__connection.close()
