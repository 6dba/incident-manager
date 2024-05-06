"""
Прикладной код, связанный с обработкой событий
"""
__author__ = "6dba"
__date__ = "04/05/2024"

from enum import Enum

from propan import RabbitBroker
from propan.brokers.rabbit import RabbitExchange, ExchangeType, RabbitQueue

from core.settings import settings


def exchange(e: str) -> RabbitExchange:
    """
    Получение существующего обменника

    :param str e: Название обменника
    :return: Объект RabbitExchange
    """
    return RabbitExchange(e, auto_delete=True, type=ExchangeType.FANOUT)


def queue(q: str) -> RabbitQueue:
    """
    Получение очереди сервиса

    :param str q: Название очереди сервиса
    :return: Объект RabbitQueue
    """
    return RabbitQueue(q)


def broker() -> RabbitBroker:
    """
    Экземпляр брокера RabbitBroker

    :return: Объект RabbitBroker
    """
    return RabbitBroker(settings.RABBITMQ_DSN)


class Exchanges(Enum):
    """
    Обменники сервисов, которые публикуют события
    """
    __metaclass__ = RabbitExchange

    PROCESSOR = exchange('processor')
    COLLECTOR = exchange('collector')
    MANAGER = exchange('manager')


class Queues(Enum):
    """
    Подписчики обменников
    """
    __metaclass__ = RabbitQueue

    PROCESSOR = queue('processor')
    MANAGER = queue('manager')
    NOTIFIER = queue('notifier')

