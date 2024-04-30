"""
Источник данных SIEM KOMRAD
"""
__author__ = "6dba"
__date__ = "30/04/2024"

import aiosql
import asyncio

from core.repositories.base.connection import PostgreSQLConnection
from core.repositories.base.repository import AbstractSIEMRepository
from core.settings import settings


class KOMRADRepositorySQL(AbstractSIEMRepository):
    """
    Источник данных SIEM KOMRAD, используя SQL
    """
    def __init__(self):
        super(KOMRADRepositorySQL, self).__init__()
        self.__connection = PostgreSQLConnection()
        self.__queries = aiosql.from_path(settings.SQL_PATH, settings.SQL_DRIVER)

    async def incident(self, incident_id: int):
        """
        Получение полных данных об указанном инциденте

        :param int incident_id: Идентификатор инцидента
        :return: Данные об инциденте
        """
        if not incident_id:
            return None

        async with self.__connection as conn:
            return await asyncio.run(self.__queries.get_detailed_incident(conn, incident_id))

    async def incidents(self, count: int, offset: int = None):
        """
        Получение данных об инцидентах

        :param int count: Количество инцидентов для выборки
        :param int offset: Смещение
        :return: Данные об инцидентах
        """
        raise NotImplementedError
        if not count:
            return None

        async with self.__connection as conn:
            return await asyncio.run(self.__queries._(conn, count, offset or 0))
