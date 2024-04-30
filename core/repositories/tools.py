"""
Модуль реализующий утилиты при работе с сервисом
"""
__author__ = "6dba"
__date__ = "29/04/2024"

from enum import Enum
from typing import Type

from core.repositories.base.repository import BaseRepository
from core.repositories.komrad import KOMRADRepositorySQL


class Siem(str, Enum):
    """
    Поддерживаемые SIEM системы
    """
    KOMRAD = 'KOMRAD'


class RepositoryProvider(str, Enum):
    """
    Возможные поставщики данных из SIEM систем
    """
    API = 'API'
    SQL = 'SQL'


class RepositoryFactory:
    """
    Фабрика разрешающая модель поставщика данных
    """
    __REPOSITORIES = {
        (Siem.KOMRAD.value, RepositoryProvider.SQL.value): KOMRADRepositorySQL
    }
    
    @staticmethod
    def resolve(siem: Siem = None, provider: RepositoryProvider = None):
        return RepositoryFactory.__REPOSITORIES.get((siem or '', provider or ''), BaseRepository)
