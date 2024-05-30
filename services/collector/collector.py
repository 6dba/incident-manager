"""
Сервис агрегации данных
"""
__author__ = "6dba"
__date__ = "29/04/2024"

import asyncio

from core.messaging.broker import Exchanges
from core.repositories.base.incident import IncidentModel
from core.repositories.tools import RepositoryFactory
from core.service import BaseService
from core.settings import settings


class CollectorService(BaseService):
    """
    Сервис агрегации данных
    """
    __polling_interval = settings.COLLECTOR_POLLING_FREQ_SEC

    def __init__(self):
        super().__init__()
        self.exchange = Exchanges.COLLECTOR.value
        self.provider = RepositoryFactory.resolve(settings.SIEM_NAME, settings.SIEM_PROVIDER)()
        self.__last_incident = None
        self.register_handlers()

    def register_handlers(self):
        """
        Регистрация обработчиков сервиса
        """
        super().register_handlers()

        @self.app.after_startup
        async def collect():
            await self.__collect()

    async def start(self):
        """
        Рабочий цикл сервиса
        """
        await self.app.run()

    async def __collect(self):
        """
        Периодический опрос источника данных
        """
        while True:
            # Получение новых инцидентов
            incidents = await self.__get_new_incidents()
            if not incidents:
                await asyncio.sleep(self.__polling_interval)
                continue
            # Публикация новых инцидентов
            await self.broker.publish(exchange=self.exchange, message=incidents)
            # Установка периода опроса
            await asyncio.sleep(self.__polling_interval)

    async def __get_new_incidents(self) -> list[IncidentModel]:
        """
        Получение информации о последних инцидентах

        :return: Список инцидентов
        """
        if not self.__last_incident:
            # Если нет информации о последнем инциденте, то запрашиваем и сохраняем по нему информацию
            # Наблюдение за новыми инцидентами будет идти от него
            last_incident = await self.provider.incidents(limit=1)
            if not last_incident:
                return []
            self.__last_incident = last_incident[0]

        new_incidents = await self.provider.incidents(last_incident_id=self.__last_incident.id)
        if not new_incidents:
            return []

        self.__last_incident = new_incidents[0]
        return new_incidents
