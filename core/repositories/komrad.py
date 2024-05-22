"""
Источник данных SIEM KOMRAD
"""
__author__ = "6dba"
__date__ = "30/04/2024"

import aiosql
from typing import Any

from core.repositories.base.connection import PostgreSQLConnection
from core.repositories.base.incident import IncidentModel
from core.repositories.base.repository import BaseSiemRepository
from core.settings import settings


class KOMRADRepositorySQL(BaseSiemRepository):
    """
    Источник данных SIEM KOMRAD посредством API на уровне SQL
    """
    def __init__(self):
        super().__init__()
        self.__connection = PostgreSQLConnection()
        self.__queries = aiosql.from_path(settings.SQL_PATH, 'asyncpg')

    async def incident(self, incident_id: int):
        """
        Получение полных данных об указанном инциденте

        :param int incident_id: Идентификатор инцидента
        :return: Данные об инциденте
        """
        if not incident_id:
            return None

        async with self.__connection as conn:
            return self._unification(await self.__queries.get_detailed_incident(conn, incident_id=incident_id))

    async def incidents(self, limit: int = 10, offset: int = 0, last_incident_id: int = 0):
        """
        Получение данных об инцидентах

        :param last_incident_id: Идентификатор последнего инцидента
        :param int limit: Количество инцидентов для выборки
        :param int offset: Смещение
        :return: Данные об инцидентах
        """
        async with self.__connection as conn:
            incidents = await self.__queries.get_last_incidents(
                conn, limit=limit, offset=offset, last_incident_id=last_incident_id
            )
            return [self._unification(incident) for incident in incidents]

    def _unification(self, incident: Any) -> IncidentModel:
        """
        Унификация данных об инциденте

        :param incident:
        :return:
        """
        return IncidentModel(**dict(incident))
