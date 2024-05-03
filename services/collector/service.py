"""
Сервис агрегации данных
"""
__author__ = "6dba"
__date__ = "29/04/2024"

import asyncio
from propan.brokers.rabbit import RabbitExchange, ExchangeType

from core.repositories.base.incident import IncidentModel
from core.repositories.tools import RepositoryFactory
from core.service import BaseService, Exchanges
from core.settings import settings, broker


class CollectorService(BaseService):
    """
    Сервис агрегации данных
    """
    _polling_interval = 60  # Частота опроса источника данных

    def __init__(self):
        super().__init__()
        # Обменник, в который сервис публикует события
        self._exchange = RabbitExchange(Exchanges.COLLECTOR, type=ExchangeType.FANOUT)
        self.__last_incident = None
        self._provider = RepositoryFactory.resolve(settings.SIEM_NAME, settings.SIEM_PROVIDER)()

    async def __get_new_incidents(self) -> list[IncidentModel]:
        """
        Получение информации о последних инцидентах

        :return: Список инцидентов
        """
        if not self.__last_incident:
            # Если нет информации о последнем инциденте, то запрашиваем и сохраняем по нему информацию
            # Наблюдение за новыми инцидентами будет идти от него
            last_incident = await self._provider.incidents(limit=1)
            if not last_incident:
                return []
            self.__last_incident = last_incident[0]

        new_incidents = await self._provider.incidents(last_incident_id=self.__last_incident.id)
        if not new_incidents:
            return []

        self.__last_incident = new_incidents[0]
        return new_incidents

    async def work(self):
        """
        Основной рабочий цикл сервиса
        """
        # Периодический опрос источника данных
        while True:
            # Получение новых инцидентов
            incidents = await self.__get_new_incidents()
            if not incidents:
                await asyncio.sleep(CollectorService._polling_interval)
                continue
            async with broker:
                # Публикация новых инцидентов
                await broker.publish(exchange=self._exchange, message=incidents)
            # Установка периода опроса
            await asyncio.sleep(CollectorService._polling_interval)
