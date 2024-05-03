"""
Источник данных SIEM KOMRAD
"""
__author__ = "6dba"
__date__ = "30/04/2024"

from typing import Any

import aiosql
import asyncio

from core.repositories.base.connection import PostgreSQLConnection
from core.repositories.base.incident import IncidentModel
from core.repositories.base.repository import BaseSiemRepository
from core.settings import settings


class KOMRADRepositorySQL(BaseSiemRepository):
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
            return await asyncio.run(self.__queries.get_detailed_incident(conn, incident_id=incident_id))

    async def incidents(self, count: int, offset: int = 0):
        """
        Получение данных об инцидентах

        :param int count: Количество инцидентов для выборки
        :param int offset: Смещение
        :return: Данные об инцидентах
        """
        async with self.__connection as conn:
            return await self.__queries.get_incidents(conn, count=count, offset=offset)

    def unification(self, incident: Any) -> IncidentModel:
        """
        Унификация данных об инциденте

        :param incident:
        :return:
        """
        return IncidentModel(**dict(incident))
