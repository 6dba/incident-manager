"""

"""

__author__ = "6dba"
__date__ = "28/04/2024"

from abc import ABC, abstractmethod

from core.repositories.tools import RepositoryFactory


class AbstractService(ABC):
    @abstractmethod
    def _startup(self): raise NotImplementedError

    @abstractmethod
    def _shutdown(self): raise NotImplementedError

    @abstractmethod
    def work(self): raise NotImplementedError


class BaseService(AbstractService):
    """
    Базовый сервис
    """
    def __init__(self):
        self._startup()

    def __del__(self):
        self._shutdown()

    def _startup(self):
        """
        Действия при запуске сервиса
        """
        return None

    def _shutdown(self):
        """
        Действия при остановке сервиса
        """

    def work(self):
        """
        Основной рабочий цикл сервиса
        """
        return None
