import asyncio
from services.collector.collector import CollectorService

if __name__ == '__main__':
    # Инициализация и запуск сервиса
    asyncio.run(CollectorService().start())
