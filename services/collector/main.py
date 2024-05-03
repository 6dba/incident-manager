import asyncio
from services.collector.service import CollectorService

if __name__ == '__main__':
    # Инициализация и запуск сервиса
    asyncio.run(CollectorService().work())
