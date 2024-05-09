"""
Сервис нотификаций
"""
__author__ = "6dba"
__date__ = "06/05/2024"

from core.messaging.broker import Exchanges, Queues
from core.repositories.base.incident import IncidentModel
from core.service import BaseService


class NotifierService(BaseService):
    """
    Сервис нотификаций и внешнего взаимодействия
    """
    def __init__(self):
        super().__init__()
        # Обменник, в который сервис публикует события
        self.queue = Queues.NOTIFIER.value
        self.register_handlers()

    def register_handlers(self):
        """
        Регистрация обработчиков сервиса
        """
        @self.broker.handle(self.queue, Exchanges.MANAGER.value)  # Подписываемся на события сервиса сбора данных
        async def notify(incidents: list[IncidentModel]):
            # Написать какой-нибудь смтп отправщик сообщений
            for incident in incidents:
                print(incident)

    async def start(self):
        """
        Рабочий цикл сервиса
        """
        await self.app.run()
