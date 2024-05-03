"""
Абстракция репозитория
"""

__author__ = "6dba"
__date__ = "28/04/2024"

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from core.repositories.base.incident import IncidentModel


class AbstractSiemRepository(ABC):
    @abstractmethod
    async def incident(self, incident_id: int | UUID): raise NotImplementedError

    @abstractmethod
    async def incidents(self, count: int, offset: int = None): raise NotImplementedError

    @abstractmethod
    def unification(self, incident: Any) -> IncidentModel: raise NotImplementedError


class BaseSiemRepository(AbstractSiemRepository):
    """
    Базовый репозиторий для получения данных из SIEM систем
    """
    @abstractmethod
    async def incident(self, incident_id: int | UUID): return None

    @abstractmethod
    async def incidents(self, count: int, offset: int = None): return None

    @abstractmethod
    def unification(self, incident: Any) -> IncidentModel: return IncidentModel()
