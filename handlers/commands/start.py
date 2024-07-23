from create_bot import dp, bot 
from aiogram import types
from data.users_db import *



@dp.message_handler(commands=["start"])
async def start_cmd(message: types.message):
    
    greeting = """
Добро пожаловать в бота "MedAsk"! 

🌸 Мы созданы с любовью для врачей-гинекологов, чтобы облегчить вашу повседневную практику и сделать ваши процессы более эффективными.

🔍 Наш бот обеспечивает не только удобный доступ к файлам, но и функционал различных калькуляторов и алгоритмов, помогая вам в точном диагнозе и эффективном лечении пациентов.

Не стесняйтесь использовать бота для получения актуальных данных, обмена опытом с коллегами и повышения эффективности вашей работы. Мы здесь, чтобы поддерживать вас в каждом шаге!

С уважением,
Команда "MedAsk" 🌟

<b>Перейдите в</b> /menu <b>для доступа к дополнительным функциям.</b>
"""

    user_id=message.from_user.id
    user = message.from_user  # Получаем объект пользователя из сообщения
    if user.username:
        username = user.username
    else:
        username = None
        
    
    await create_profile(user_id=user_id, nickname=username)
    await message.answer(greeting, parse_mode = "HTML")