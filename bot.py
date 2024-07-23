from aiogram.utils import executor
from create_bot import dp
from handlers.commands import *
from data.users_db import users_db_start
from data.info_db import info_db_start
from data.config import BOT_TOKEN
from NN.health_risk import initialize_model  # Импортируем функцию для запуска модели НС

async def on_startup(_):
    await users_db_start() #Инициализируем БД пользователей
    await info_db_start() # Инициализируем БД с файлами
    await initialize_model()  # Инициализируем модель нейронной сети
    print("Бот запущен, подключение к БД выполнено успешно и модель инициализирована")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
