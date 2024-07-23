from create_bot import dp, bot 
from aiogram import types  
from keyboards.files_kb import create_files_kb
from aiogram.dispatcher import FSMContext
from keyboards.menu_kb import create_menu_kb


# Обработчик команды "/menu"
@dp.message_handler(commands=['menu'], state="*")
async def menu_command(message: types.Message, state: FSMContext):
    menu_text = "Вы находитесь в главном меню. Пожалуйста, выберите нужное действие."
    await state.finish()
    await message.delete()  # Удаление исходного сообщения, содержащего команду "/menu"

    # Отправка сообщения с текстом меню и клавиатурой, полученной из функции 'get_menu_kb_class'
    await bot.send_message(chat_id=message.from_user.id,
                            text=menu_text,
                            reply_markup=create_menu_kb())
    
# Обработчик для кнопки "Файлы"
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'files')
async def process_files_button(callback_query: types.CallbackQuery):
    # Отправляем сообщение с текстом и клавиатурой
    await bot.send_message(callback_query.from_user.id, "Выберите нужную категорию:", reply_markup=create_files_kb())
