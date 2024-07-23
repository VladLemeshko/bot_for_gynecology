from create_bot import dp, bot
from aiogram import types, exceptions


from data.info_db import get_data_for_selected_object

import base64
import io

 # Функция для декодирования BLOB-данных
def decode_blob(blob_data):
    return base64.b64decode(blob_data)

@dp.message_handler(lambda message: message.text.startswith('-'))
async def info_more_callback(message: types.Message):
    obj_id = message.text.split('- ')[1]
    obj_data = await get_data_for_selected_object(obj_id)

    if obj_data:
        short_name, full_name, form_pdf = obj_data
        decoded_pdf = decode_blob(form_pdf)
        pdf_io = io.BytesIO(decoded_pdf)

        # Проверяем магическое число для определения формата файла
        if decoded_pdf.startswith(b"%PDF"):
            # Отправляем только если это PDF
            try:
                # Используем InputFile для отправки файла
                await bot.send_document(
                    message.chat.id,
                    document=types.InputFile(pdf_io, filename=f"{full_name}.pdf"),
                    caption=full_name
                )
            except exceptions.BadRequest as e:
                # Обработка исключения, например, если пользователь отключил уведомления о документах
                print(f"Exception while sending document: {e}")
        else:
            await message.answer("Файл не имеет формат PDF.")