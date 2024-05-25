__author__ = "6dba"
__date__ = "28/04/2024"

import logging
from abc import ABC, abstractmethod
from propan import PropanApp

from core.messaging.broker import broker


class AbstractService(ABC):
    @abstractmethod
    def register_handlers(self): raise NotImplementedError

    @abstractmethod
    async def start(self): raise NotImplementedError


class BaseService(AbstractService):
    """
    Базовый сервис
    """
    def __init__(self):
        self.logger = logging.getLogger(type(self).__name__)
        self.broker = broker()
        self.app = PropanApp(self.broker)

    def register_handlers(self):
        """
        Регистрация обработчиков сервиса
        """
        return None

    async def start(self):
        """
        Рабочий цикл сервиса
        """
        return None
