from create_bot import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from states.admin_states import *
from data.config import is_admin
from keyboards.admin_kb import get_admin_keyboard, get_adminmode_keyboard
from data.info_db import add_new_info

import base64
import io

 # Словарь сопоставления русских и английских названий
function_mapping = {
    "Анкета": "form",
    "Шкала": "scale",
    "Показание": "testimony",
    "Критерий оценки качества": "grade",
}
 
# Обработчик команды /admin
@dp.message_handler(lambda message: message.text in ["/admin", "Панель администратора"], state="*")
async def admin_panel(message: types.Message, state: FSMContext):
    await state.finish()
    if is_admin(message.from_user.id):
        # Пользователь - администратор
        await message.answer("Вы находитесь в панели управления администратора, пожалуйста, выберите действие на клавиатуре:",
                             reply_markup=get_admin_keyboard())
    else:
        # Пользователь не является администратором
        await message.answer("Вы не являетесь администратором")
        
            
@dp.message_handler(lambda message: message.text in function_mapping.keys())
async def add_form(message: types.Message, state: FSMContext):
    if is_admin(message.from_user.id):
        await message.answer("Введите короткое название(аббревиатура), которое хотите добавить:", reply_markup=get_adminmode_keyboard())
        await ItemAddStates.add_short_name_state.set()
        async with state.proxy() as data:
            data["selected_function"] = function_mapping[message.text]  # Используйте словарь для получения английского названия
    else:
        await message.answer("Вы не являетесь администратором")

@dp.message_handler(state=ItemAddStates.add_short_name_state)
async def process_add_short_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
            data["add_short_name"] = message.text

    await message.answer("Введите полное название, которое хотите добавить:", reply_markup=get_adminmode_keyboard())
    
    await ItemAddStates.add_full_name_state.set()
    
@dp.message_handler(state=ItemAddStates.add_full_name_state)
async def process_add_full_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
            data["add_full_name"] = message.text

    await message.answer("Введите ключевые слова через запятую, которые хотите добавить:", reply_markup=get_adminmode_keyboard())
    
    await ItemAddStates.add_keywords_state.set()
    
@dp.message_handler(state=ItemAddStates.add_keywords_state)
async def process_add_keywords(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
            data["add_keywords"] = message.text

    await message.answer("Отправьте PDF-файл, который хотите добавить", reply_markup=get_adminmode_keyboard())
    
    await ItemAddStates.add_pdf_state.set()
    
@dp.message_handler(state=ItemAddStates.add_pdf_state, content_types=types.ContentType.DOCUMENT)
async def process_add_pdf(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pdf_file = await message.document.download()  # Скачиваем файл локально

        with open(pdf_file.name, "rb") as file:
            pdf_content = file.read()
            data["add_pdf"] = base64.b64encode(pdf_content).decode('utf-8')

        short_name = data["add_short_name"]
        full_name = data["add_full_name"]
        keywords = data['add_keywords']
        pdf = data['add_pdf']
        
        # Определение словаря с функциями базы данных для каждого типа элемента
        db_functions = ['grade','scale', 'testimony', 'form']

        selected_function = data.get('selected_function')
        if selected_function in db_functions:
            await add_new_info(short_name=short_name, full_name=full_name, key_words=keywords, form_pdf=pdf, type=selected_function)
            await message.answer(f"Элемент \"{full_name}\" успешно добавлен!", reply_markup=get_adminmode_keyboard())
        else:
            await message.answer(f"Ошибка: Неизвестный тип элемента \"{selected_function}\"", reply_markup=get_adminmode_keyboard())


    await state.finish()
        

# Функция для декодирования BLOB-данных
def decode_blob(blob_data):
    return base64.b64decode(blob_data)

# Обработчик, который выводит информацию о первой записи из БД
@dp.message_handler(Command("показать"))
async def show_first_record(message: types.Message):
    result = []

    if result:
        short_name, full_name, form_pdf = result

        # Декодирование BLOB-данных из form_pdf
        decoded_pdf = decode_blob(form_pdf)

        # Здесь вы можете использовать decoded_pdf по своему усмотрению, например, отправить как файл
        # В данном примере, мы отправляем декодированный PDF как документ
        pdf_io = io.BytesIO(decoded_pdf)
        pdf_io.name = f"{short_name}.pdf"
        await message.answer_document(pdf_io, caption=f"{short_name}: {full_name}\n")
    else:
        await message.answer("Форма не найдена.")