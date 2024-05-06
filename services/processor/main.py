import asyncio

from services.processor.processor import ProcessorService

if __name__ == '__main__':
    # Инициализация и запуск сервиса
    asyncio.run(ProcessorService().start())
