import asyncio
from services.manager.manager import ManagerService

if __name__ == '__main__':
    # Инициализация и запуск сервиса
    asyncio.run(ManagerService().start())
