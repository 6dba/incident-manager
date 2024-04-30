"""
Утилиты при работе с сервисом
"""
__author__ = "6dba"
__date__ = "29/04/2024"

from enum import Enum

from core.repositories.base.repository import BaseRepository
from core.repositories.komrad import KOMRADRepositorySQL


class Siem(str, Enum):
    """
    Поддерживаемые SIEM
    """
    KOMRAD = 'KOMRAD'


class RepositoryProvider(str, Enum):
    """
    Возможные способы поставки данных из SIEM
    """
    API = 'API'
    SQL = 'SQL'


class RepositoryFactory:
    """
    Фабрика, разрешающая модель поставщика данных
    """
    __REPOSITORIES = {
        (Siem.KOMRAD.value, RepositoryProvider.SQL.value): KOMRADRepositorySQL
    }
    
    @staticmethod
    def resolve(siem: Siem = None, provider: RepositoryProvider = None):
        """
        Разрешает поставщика данных в зависимости от SIEM и способа получения данных

        :param Siem siem: Поддерживаемая SIEM
        :param RepositoryProvider provider: Поддерживаемый способ поставки данных
        :return: Репозиторий
        """
        return RepositoryFactory.__REPOSITORIES.get((siem or '', provider or ''), BaseRepository)
