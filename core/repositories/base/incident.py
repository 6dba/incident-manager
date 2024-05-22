"""
Модель инцидента
"""
__author__ = "6dba"
__date__ = "03/05/2024"

import re
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, computed_field


class SeverityEnum(str, Enum):
    """
    Критичность инцидента
    """
    BASELINE = 'baseline'
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class StatusEnum(str, Enum):
    """
    Статус инцидента
    """
    NEW = 'new'
    INVESTIGATING = 'investigating'
    CLOSED = 'closed'
    FALSE = 'fp'


class GossopkaSendingStatusEnum(str, Enum):
    """
    Статус отправки в ГосСОПКА
    """
    IGNORE = 'ignore'
    WAITING = 'waiting'
    SUCCESS = 'success'
    FAILED = 'failed'


class IncidentModel(BaseModel):
    """
    Унифицированная модель инцидента
    """
    id: int
    assigned_to: str  # Ответственный
    initial_time: datetime  # Дата фактического начала инцидента
    registration_time: datetime  # Дата регистрации инцидента
    close_time: datetime | None
    status: StatusEnum
    severity: SeverityEnum
    gossopka_sending_status: GossopkaSendingStatusEnum
    recommendation: str
    updated_at: datetime | None
    comments: str
    status_reason: str  # Причина появления инцидента
    gossopka_incident_type: str
    gossopka_incident_id: str | None
    description: str
    asset_ips: list | None
    threats_array: list | None
    gossopka_incident_category: str
    response_stage: int  # Линия расследования
    checksum: str | None = None  # Контрольная сумма инцидента

    @computed_field
    @property
    def emails(self) -> list[str]:
        return re.findall(r"[0-9a-zA-z]+@[0-9a-zA-z]+\.[0-9a-zA-z]+", self.assigned_to)

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.dict() == other.dict()
