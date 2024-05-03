"""

"""

__author__ = "6dba"
__date__ = "28/04/2024"

from abc import ABC, abstractmethod
from enum import Enum


class Exchanges(str, Enum):
    """
    Обменники сервисов, которые публикуют события
    """
    COLLECTOR = 'collector'


class AbstractService(ABC):
    @abstractmethod
    def _startup(self): raise NotImplementedError

    @abstractmethod
    def _shutdown(self): raise NotImplementedError

    @abstractmethod
    async def work(self): raise NotImplementedError


class BaseService(AbstractService):
    """
    Базовый сервис
    """
    # Обменник сервиса
    EXCHANGE = None

    def __init__(self):
        self._startup()

    def __del__(self):
        self._shutdown()

    def _startup(self):
        """
        Запуск сервиса
        """
        return None

    def _shutdown(self):
        """
        Остановка сервиса
        """
        return None

    async def work(self):
        """
        Рабочий цикл сервиса
        """
        return None
