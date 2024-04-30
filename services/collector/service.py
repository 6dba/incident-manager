"""
Сервис агрегации данных
"""
__author__ = "6dba"
__date__ = "29/04/2024"

from core.repositories.tools import RepositoryFactory
from core.service import BaseService
from core.settings import settings


class CollectorService(BaseService):
    """
    Сервис агрегации данных
    """
    def __init__(self):
        super().__init__()
        self._provider = RepositoryFactory.resolve(settings.SIEM_NAME, settings.SIEM_PROVIDER)()

    def work(self):
        """

        :return:
        """

