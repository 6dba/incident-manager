"""
Сервис классификации и пост обработки данных
"""
__author__ = "6dba"
__date__ = "29/04/2024"

from core.messaging.broker import Exchanges, Queues
from core.repositories.base.incident import IncidentModel
from core.service import BaseService


class ProcessorService(BaseService):
    """
    Сервис классификации и пост обработки данных
    """
    def __init__(self):
        super().__init__()
        self.queue = Queues.PROCESSOR.value
        self.exchange = Exchanges.PROCESSOR.value
        self.register_handlers()

    def register_handlers(self):
        """
        Регистрация обработчиков сервиса
        """
        @self.broker.handle(self.queue, Exchanges.COLLECTOR.value)  # Подписываемся на события сервиса сбора данных
        async def process(incidents: list[IncidentModel]):
            await self.__process(incidents)

    async def __process(self, incidents: list[IncidentModel]):
        """
        Пост-обработка инцидента

        :param list[IncidentModel] incidents: Список инцидентов
        """
        # Публикация новых инцидентов
        await self.broker.publish(exchange=self.exchange, message=incidents)

    async def start(self):
        """
        Рабочий цикл сервиса
        """
        await self.app.run()
