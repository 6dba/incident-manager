"""
Сервис файловой обработки инцидентов
"""
__author__ = "6dba"
__date__ = "07/05/2024"

import os
import glob
import ftplib
from docx import Document

from core.messaging.broker import Exchanges, Queues
from core.repositories.base.incident import IncidentModel, StatusEnum
from core.service import BaseService
from core.settings import settings
from services.manager.templates.messages import TO_REPLACE


class ManagerService(BaseService):
    """

    """
    def __init__(self):
        super().__init__()
        # Обменник, в который сервис публикует события
        self.exchange = Exchanges.MANAGER.value
        self.queue = Queues.MANAGER.value
        self.__template_pattern = r'templates/*.docx'
        # {Название шаблона: Путь к файлу шаблона}
        self.templates = {os.path.basename(p).removesuffix('.docx'): p for p in glob.glob(self.__template_pattern)}
        self.register_handlers()

    def register_handlers(self):
        """
        Регистрация обработчиков сервиса
        """
        @self.broker.handle(self.queue, Exchanges.PROCESSOR.value)  # Подписка события сервиса пост-обработки данных
        async def manage(incidents: list[IncidentModel]):
            await self.__manage(incidents)

    async def __manage(self, incidents: list[IncidentModel]):
        """
        Обработка инцидентов, заполнение шаблона

        :param list[IncidentModel] incidents:
        """
        processed = []
        for incident in incidents:
            doc = self.__resolve_document(incident)
            table = doc.tables[0]
            # Заполнение таблицы документа, по данным инцидента
            self.__process_table(incident, table)
            # Опубликовать событие или сохранить файл и опубликовать событие с ним
            processed.append(incident)

        if processed:
            # Если появились обработанные документы - публикуем связанные с ними инциденты,
            # как способ сказать о том, какие инциденты были обработаны менеджером
            await self.broker.publish(exchange=self.exchange, message=processed)

    def to_ftp(self, documents: list[Document]):
        """

        :param documents:
        :return:
        """
        session = ftplib.FTP(settings.FTP_HOST, settings.FTP_USER, settings.FTP_PASSWORD)

        for document in documents:
            pass

    @staticmethod
    def __process_table(incident: IncidentModel, table: Document):
        """
        Заполнение таблицы документа, по данным инцидента

        :param IncidentModel incident:
        :param table:
        :return:
        """
        replaced_titles = []

        for row in table.rows:
            # Колонка с названием строки
            title = row.cells[0].text

            if title in replaced_titles:
                # Особенности строки с двумя колонками, когда вторая колонка содержит несколько строк,
                # которые по логике таблицы относятся к одной строке
                # _________________________________________________________________________________
                #                                         | Да
                # Необходимость привлечения сил ГосСОПКА  -----------------------------------------
                #                                         | Нет
                # _________________________________________________________________________________
                # Итерация по ячейкам в таком случае происходит попарно, то есть фактически строк будет две:
                # ('Необходимость привлечения сил ГосСОПКА', 'Да'), ('Необходимость привлечения сил ГосСОПКА', 'Нет')
                # Соответственно при первой итерации, выбираем нужно значение,
                # а при второй итерации - удаляем уже обработанную строку
                table._tbl.remove(row._tr)
                continue

            replaced = TO_REPLACE.get(title, lambda _: None)(incident)
            if not replaced:
                # Если для данной строки не нужно производить замен
                continue

            row.cells[1].text = replaced
            replaced_titles.append(title)

    def __resolve_document(self, incident: IncidentModel) -> Document:
        """
        Разрешение документа-шаблона для инцидента
        :param IncidentModel incident:
        :return: Объект документа .docx
        :rtype: Document
        :raise: ValueError
        """
        if incident.gossopka_incident_type.lower() not in list(map(lambda t: t.lower(), self.templates.keys())):
            # Если тип инцидента не соответствует ни одному шаблону
            raise ValueError

        # Создаем объект документа для выбранного шаблона
        return Document(self.templates.get(incident.gossopka_incident_type, ''))

    async def start(self):
        """
        Рабочий цикл сервиса
        """
        await self.app.run()

