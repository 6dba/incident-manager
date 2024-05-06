import asyncio
from services.notifier.notifier import NotifierService

if __name__ == '__main__':
    # Инициализация и запуск сервиса
    asyncio.run(NotifierService().start())
