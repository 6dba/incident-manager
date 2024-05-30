"""

"""
__author__ = "6dba"
__date__ = "08/05/2024"

from enum import Enum

from core.repositories.base.incident import StatusEnum, GossopkaSendingStatusEnum


class DocAnswerMessageEnum(str, Enum):
    """
    Поля для шаблонных ответов документа
    """
    GOSSOPKA_YES = 'Да'
    GOSSOPKA_NO = 'Нет'

    STATUS_CLOSED = 'Меры приняты, атака локализована'
    STATUS_INVESTIGATED = 'Проводятся мероприятия по локализации компьютерной атаки'
    STATUS_AGAIN = 'Возобновлены мероприятия по локализации компьютерной атаки'

    COUNTRY = 'Россия'


class DocCellMessageEnum(str, Enum):
    """
    Поля для замены в документе-шаблоне
    """
    STATUS = 'Статус реагирования'
    GOSSOPKA = 'Необходимость привлечения сил ГосСОПКА'
    DESCRIPTION = 'Краткое описание события ИБ'
    REGISTRATION_TIME = 'Дата и время выявления'
    CLOSE_TIME = 'Дата и время завершения'
    ASSET_IPv4S = 'IPv4-адрес (маршрутизируемый) атакованного ресурса'
    REGION = 'Страна/Регион'
    OTHER = 'Дополнительные значимые сведения о компьютерной атаке (в свободной форме)'
    THREATS = 'Описание используемых уязвимостей'
    APPLICANT = 'Заявитель'


TO_REPLACE = {
    k.strip().lower(): v for k, v in {
        DocCellMessageEnum.STATUS: lambda incident: {
            StatusEnum.CLOSED: DocAnswerMessageEnum.STATUS_CLOSED,
            StatusEnum.NEW: DocAnswerMessageEnum.STATUS_INVESTIGATED,
            StatusEnum.INVESTIGATING: DocAnswerMessageEnum.STATUS_INVESTIGATED
        }.get(incident.status),
        DocCellMessageEnum.GOSSOPKA: lambda incident: {
            GossopkaSendingStatusEnum.SUCCESS: DocAnswerMessageEnum.GOSSOPKA_YES,
            GossopkaSendingStatusEnum.WAITING: DocAnswerMessageEnum.GOSSOPKA_YES,
            GossopkaSendingStatusEnum.FAILED: DocAnswerMessageEnum.GOSSOPKA_NO,
            GossopkaSendingStatusEnum.IGNORE: DocAnswerMessageEnum.GOSSOPKA_NO
        }.get(incident.gossopka_sending_status),
        DocCellMessageEnum.DESCRIPTION:
            lambda incident:
            (incident.description or '') + f'\n\nКонтрольная сумма по алгоритму Стрибог 256: {incident.checksum}',
        DocCellMessageEnum.REGISTRATION_TIME: lambda incident: str(incident.registration_time),
        DocCellMessageEnum.CLOSE_TIME: lambda incident: str(incident.close_time) if incident.close_time else None,
        DocCellMessageEnum.ASSET_IPv4S: lambda incident: incident.asset_ips,
        DocCellMessageEnum.REGION: lambda _: DocAnswerMessageEnum.COUNTRY,
        DocCellMessageEnum.OTHER: lambda incident: incident.comments,
        DocCellMessageEnum.THREATS: lambda incident: incident.threats_array,
        DocCellMessageEnum.APPLICANT: lambda incident: incident.assigned_to
    }.items()
}
