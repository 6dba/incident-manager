import aiosql, asyncio

from core.repositories.base.connection import PostgreSQLConnection
from core.repositories.base.repository import AbstractRepository
from core.settings import settings


class KOMRADRepositorySQL(AbstractRepository):
    """

    """
    def __init__(self):
        super(KOMRADRepositorySQL, self).__init__()
        self.__connection = PostgreSQLConnection()
        self.__queries = aiosql.from_path(settings.SQL_PATH, settings.SQL_DRIVER)

    async def incident(self, incident_id: int):
        """
        Получение полных данных об инциденте

        :param incident_id:
        :return:
        """
        if not incident_id:
            return None

        async with self.__connection as conn:
            return await asyncio.run(self.__queries.get_detailed_incident(conn, incident_id))

    async def incidents(self, count: int, offset: int = None):
        """
        Получение данных об инцидентах

        :param count:
        :param offset:
        :return:
        """
        raise NotImplementedError
        if not count:
            return None

        async with self.__connection as conn:
            return await asyncio.run(self.__queries._(conn, count, offset or 0))
