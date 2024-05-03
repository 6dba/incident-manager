from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


class StatusEnum(str, Enum):
    """
    Статус инцидента
    """
    NEW = 'new'


class SeverityEnum(str, Enum):
    """
    Критичность инцидента
    """
    HIGH = 'high'


class IncidentModel(BaseModel):
    """
    Унифицированная модель инцидента
    """
    id: int
    gossopka: Any
    gossopka_sending_status: str
    assigned_to: str
    is_retro: bool
    initial_time: datetime
    registration_time: datetime
    # close_time: datetime = None
    status: StatusEnum
    severity: SeverityEnum
    recommendation: str
    description: str
    gossopka_incident_category: str

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.dict() == other.dict()

    # 'name' = {NoneType} None
    #  'directive_severity' = {NoneType} None
    #  'id' = {int} 1
    #  'directive_id' = {NoneType} None
    #  'directive_assigned_to' = {NoneType} None
    #  'reaction_script_filename' = {NoneType} None
    #  'reaction_is_enabled' = {NoneType} None
    #  'created_at' = {NoneType} None
    #  'directive_updated_at' = {NoneType} None
    #  'aggregate_in' = {NoneType} None
    #  'aggregated_min_count' = {NoneType} None
    #  'group_id' = {NoneType} None
    #  'gossopka' = {NoneType} None
    #  'directive_recommendation' = {NoneType} None
    #  'aggregate_greedily_count' = {NoneType} None
    #  'directive_gossopka_incident_type' = {NoneType} None
    #  'rule' = {NoneType} None
    #  'deleted_at' = {NoneType} None
    #  'risk_score' = {NoneType} None
    #  'author' = {NoneType} None
    #  'reference_url' = {NoneType} None
    #  'note' = {NoneType} None
    #  'timestamp_override' = {NoneType} None
    #  'rule_edit_state' = {NoneType} None
    #  'produce_incident' = {NoneType} None
    #  'produce_aggregated_event' = {NoneType} None
    #  'store_keys_in_event' = {NoneType} None
    #  'directive_threats_array' = {NoneType} None
    #  'directive_gossopka_incident_category' = {NoneType} None
    #  'assigned_to' = {str} 'Фамилия admin Отчество - admin@admin.ru'
    #  'is_retro' = {bool} False
    #  'initial_time' = {datetime} datetime.datetime(2024, 5, 3, 8, 27, 43, tzinfo=datetime.timezone.utc)
    #  'registration_time' = {datetime} datetime.datetime(2024, 5, 3, 8, 32, 35, 560364, tzinfo=datetime.timezone.utc)
    #  'close_time' = {NoneType} None
    #  'status' = {str} 'new'
    #  'severity' = {str} 'high'
    #  'event_doc_keys' = {list: 1} ['0000000066349fff0000001d00000008']
    #  'gossopka_sending_status' = {str} 'ignore'
    #  'security_label' = {int} 0
    #  'tenant_id' = {int} 0
    #  'correlator_ids' = {list: 0} []
    #  'recommendation' = {str} ''
    #  'has_errors' = {bool} False
    #  'updated_at' = {NoneType} None
    #  'comments' = {str} '{}'
    #  'status_reason' = {str} ''
    #  'histories' = {list: 1} ['[{"EventDocKey":"1714724863-0000001d-00000008","StepID":"manual","Error":"","CommandResult":"next"}]']
    #  'gossopka_incident_type' = {str} 'Вовлечение контролируемого ресурса в инфраструктуру ВПО'
    #  'gossopka_incident_id' = {NoneType} None
    #  'response_stage' = {int} 1
    #  'description' = {str} 'аааааааааааааааааааааа пизда рулям'
    #  'asset_ips' = {NoneType} None
    #  'threats_array' = {NoneType} None
    #  'gossopka_incident_category' = {str} 'Уведомление о компьютерном инциденте'

