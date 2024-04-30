"""
Абстракция репозитория
"""

__author__ = "6dba"
__date__ = "28/04/2024"

from abc import ABC, abstractmethod
from uuid import UUID


class AbstractSIEMRepository(ABC):
    @abstractmethod
    async def incident(self, incident_id: int | UUID): raise NotImplementedError

    @abstractmethod
    async def incidents(self, count: int, offset: int = None): raise NotImplementedError
