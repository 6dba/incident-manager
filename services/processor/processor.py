"""
Сервис классификации и пост обработки данных
"""
__author__ = "6dba"
__date__ = "29/04/2024"

from gostcrypto import gosthash

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
        @self.broker.handle(self.queue, Exchanges.COLLECTOR.value)  # Подписка на события сервиса сбора данных
        async def process(incidents: list[IncidentModel]):
            await self.__process(incidents)

    async def __process(self, incidents: list[IncidentModel]):
        """
        Пост-обработка инцидента

        :param list[IncidentModel] incidents: Список инцидентов
        """
        for incident in incidents:
            if not incident.checksum:
                # Вычисление контрольной суммы инцидента по алгоритму Стрибог 256 ГОСТ 34.11-2018.
                incident.checksum = gosthash.new(
                    'streebog256', data=incident.json(sort_keys=True).encode()
                ).hexdigest()
        # Публикация новых инцидентов
        await self.broker.publish(exchange=self.exchange, message=incidents)

    async def start(self):
        """
        Рабочий цикл сервиса
        """
        await self.app.run()
