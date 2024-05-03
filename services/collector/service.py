"""
Сервис агрегации данных
"""
__author__ = "6dba"
__date__ = "29/04/2024"

import asyncio

from core.repositories.tools import RepositoryFactory
from core.service import BaseService, Exchanges
from core.settings import settings, broker


class CollectorService(BaseService):
    """
    Сервис агрегации данных
    """
    POLLING_INTERVAL = 60
    EXCHANGE = "collector"

    def __init__(self):
        super().__init__()
        self.__last_incident = None
        self._provider = RepositoryFactory.resolve(settings.SIEM_NAME, settings.SIEM_PROVIDER)()

    async def work(self):
        """
        Основной рабочий цикл сервиса
        """
        # Периодический опрос источника данных
        while True:
            # Получение инцидентов
            incidents = await self._provider.incidents(5)
            if not incidents:
                await asyncio.sleep(CollectorService.POLLING_INTERVAL)
                continue
            incidents = [self._provider.unification(incident) for incident in incidents]

            # Если есть новые инциденты - публикуем их
            if incidents[0] != self.__last_incident:
                self.__last_incident = incidents[0]
                await broker.publish(exchange=Exchanges.COLLECTOR, message=incidents)
            await asyncio.sleep(CollectorService.POLLING_INTERVAL)
