"""

"""
__author__ = "6dba"
__date__ = "08/05/2024"

from enum import Enum

from core.repositories.base.incident import StatusEnum, GossopkaSendingStatusEnum


class DocCellMessageEnum(str, Enum):
    """

    """
    STATUS = 'Статус реагирования'
    STATUS_CLOSED = 'Меры приняты, атака локализована'
    STATUS_INVESTIGATED = 'Проводятся мероприятия по локализации компьютерной атаки'
    STATUS_AGAIN = 'Возобновлены мероприятия по локализации компьютерной атаки'

    GOSSOPKA = 'Необходимость привлечения сил ГосСОПКА'
    GOSSOPKA_YES = 'Да'
    GOSSOPKA_NO = 'Нет'

    DESCRIPTION = 'Краткое описание события ИБ'
    REGISTRATION_TIME = 'Дата и время выявления'
    CLOSE_TIME = 'Дата и время завершения'

    ASSET_IPv4S = 'IPv4-адрес (маршрутизируемый) атакованного ресурса'

    REGION = 'Страна/Регион'

    OTHER = 'Дополнительные значимые сведения о компьютерной атаке (в свободной форме)'

    THREATS = 'Описание используемых уязвимостей'

    OWNER = 'Владелец информационного ресурса'


TO_REPLACE = {
    DocCellMessageEnum.STATUS: lambda incident: {
        StatusEnum.CLOSED: DocCellMessageEnum.STATUS_CLOSED,
        StatusEnum.NEW: DocCellMessageEnum.STATUS_INVESTIGATED,
        StatusEnum.INVESTIGATING: DocCellMessageEnum.STATUS_INVESTIGATED
    }.get(incident.status),
    DocCellMessageEnum.GOSSOPKA: lambda incident: {
        GossopkaSendingStatusEnum.SUCCESS: DocCellMessageEnum.GOSSOPKA_YES,
        GossopkaSendingStatusEnum.WAITING: DocCellMessageEnum.GOSSOPKA_YES,
        GossopkaSendingStatusEnum.FAILED: DocCellMessageEnum.GOSSOPKA_NO,
        GossopkaSendingStatusEnum.IGNORE: DocCellMessageEnum.GOSSOPKA_NO
    }.get(incident.gossopka_sending_status),
    DocCellMessageEnum.DESCRIPTION: lambda incident: incident.description or '' +
                                                     f'Контрольная сумма Стрибог 256: {incident.checksum}',
    DocCellMessageEnum.REGISTRATION_TIME: lambda incident: str(incident.registration_time),
    DocCellMessageEnum.CLOSE_TIME: lambda incident: str(incident.close_time) if incident.close_time else None,
    DocCellMessageEnum.ASSET_IPv4S: lambda incident: incident.asset_ips,
    DocCellMessageEnum.REGION: lambda _: 'Россия',
    DocCellMessageEnum.OTHER: lambda incident: incident.comments,
    DocCellMessageEnum.THREATS: lambda incident: incident.threats_array,
    DocCellMessageEnum.OWNER: lambda incident: incident.assigned_to
}
