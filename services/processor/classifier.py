"""
Классификатор типа инцидента
"""
__author__ = "6dba"
__date__ = "12/05/2024"

from core.repositories.base.incident import IncidentModel


class IncidentClassifier:
    """
    Классификатор типа инцидента на основе комбинированного текста с использованием предопределенных ключевых слов
    """
    keywords = {
        ("DDoS", "отказ", "обслуживан", "атака", "денайл"): (
            "Атака DDoS", ["замедление", "slow", "замедлять", "overload", "перегрузка"],
            "Замедление работы ресурса в результате DDoS атаки"
        ),
        ("захват", "трафик", "сниф", "перехват"): (
            "Захват сетевого трафика", None, None
        ),
        ("вовлечение", "использование", "эксплуатация"): (
            "Вовлечение контролируемого ресурса в инфраструктуру ВПО", None, None
        ),
        ("заражение", "вирус", "малварь", "malware"): (
            "Заражение ВПО", None, None
        ),
        ("SQL-инъекция", "инъекция", "sql"): (
            "Попытки внедрения ВПО", None, None
        ),
        ("фишинг", "phishing", "социальная инженерия"): (
            "Использование контролируемого ресурса для фишинга", None, None
        ),
        ("компрометация", "учетная запись", "пароль", "бреач", "breach"): (
            "Компрометация учетной записи", None, None
        ),
        ("изменение", "модификация", "альтерация", "изменять"): (
            "Несанкционированное изменение информации", None, None
        ),
        ("разглашение", "утечка", "leak", "disclosure"): (
            "Несанкционированное разглашение информации", None, None
        ),
        ("неудачные попытки входа", "логин", "пароль", "authentication", "auth"): (
            "Неудачные попытки авторизации", None, None
        ),
        ("уязвимост", "уязвимость", "exploit", "vulnerability"): (
            "Попытки эксплуатации уязвимости", ["успешная", "successful"],
            "Успешная эксплуатация уязвимости"
        ),
        ("мошенническая информация", "фейк", "fake", "scam"): (
            "Публикация мошеннической информации", None, None
        ),
        ("запрещенная информация", "иллегальная", "запрет", "противозаконная"): (
            "Публикация на ресурсе запрещенной законодательством РФ информации", None, None
        ),
        ("спам", "spam", "рассылка", "mass email"): (
            "Рассылка спам-сообщений с контролируемого ресурса", None, None
        ),
        ("сканирование", "scan", "скан", "port scan"): (
            "Сетевое сканирование", None, None
        ),
        ("социальная инженерия", "social engineering", "психологическое давление"): (
            "Социальная инженерия", None, None
        ),
        ("уязвимый ресурс", "уязвимость", "vulnerable"): (
            "Уязвимый ресурс", None, None
        )
    }

    @staticmethod
    def classify(incident: IncidentModel):
        """
        Классифицировать тип инцидента по контексту модели

        :param IncidentModel incident: Модель инцидента
        """
        if incident.gossopka_incident_type:
            return
        text = f"{incident.description} {incident.comments} {incident.recommendation}".lower()
        g_type = None

        for keywords, (primary_type, alt_conditions, alternative_type) in IncidentClassifier.keywords.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    if alt_conditions and any(alt_cond.lower() in text for alt_cond in alt_conditions):
                        g_type = alternative_type
                    g_type = primary_type

        if g_type is not None:
            incident.gossopka_incident_type = g_type
