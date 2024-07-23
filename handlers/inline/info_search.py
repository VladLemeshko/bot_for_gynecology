from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle, InlineKeyboardButton, InlineKeyboardMarkup
from create_bot import dp, bot


from data.info_db import fetch_info, get_data_for_selected_object, search_for_key_words


function_mapping = {
    "анкеты": "form",
    "шкалы": "scale",
    "показания": "testimony",
    "критерии оценки качества": "grade",
}

async def create_inline_keyboard(info_id):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Подробнее", callback_data=f"info_{info_id}")
    keyboard.add(button)
    return keyboard

@dp.inline_handler()
async def inline_query_handler(inline_query: InlineQuery):
    try:
        query = inline_query.query.strip().lower()
        print(query)

        if query in ['анкеты', 'шкалы', 'показания', 'критерии оценки качества']:
            type_value = function_mapping[query]
            data = await fetch_info(type_value)
            print(data)
            results = []
            for idx, (short_name, full_name) in enumerate(data):
                description = f"{full_name}"

                input_message_content = InputTextMessageContent(
                    message_text=f' - {full_name}'  # Отображаем full_name в тексте
                )

                result = InlineQueryResultArticle(
                    id=idx,
                    title=short_name,
                    description=description,
                    input_message_content=input_message_content,
                    thumb_url='https://play-lh.googleusercontent.com/IkcyuPcrQlDsv62dwGqteL_0K_Rt2BUTXfV3_vR4VmAGo-WSCfT2FgHdCBUsMw3TPGU',  # Замените на ссылку на изображение
                )

                results.append(result)
            print(results)
            await bot.answer_inline_query(inline_query.id, results=results,
                                             cache_time=1, is_personal=True,)

        else:
            # Получаем результаты поиска по ключевым словам
            results = await search_for_key_words(query)

            print(f"Results for query '{query}': {results}")  # Отладочный print

            # Строим результаты для инлайн-режима
            inline_results = []
            for idx, (short_name, full_name) in enumerate(results):
                description = f"{full_name}"

                input_message_content = InputTextMessageContent(
                    message_text=f' - {full_name}'  # Отображаем full_name в тексте
                )

                result = InlineQueryResultArticle(
                    id=idx,
                    title=short_name,
                    description=description,
                    input_message_content=input_message_content,
                    thumb_url='https://play-lh.googleusercontent.com/IkcyuPcrQlDsv62dwGqteL_0K_Rt2BUTXfV3_vR4VmAGo-WSCfT2FgHdCBUsMw3TPGU',  # Замените на ссылку на изображение
                )

                inline_results.append(result)

            await bot.answer_inline_query(inline_query.id, results=inline_results, cache_time=1, is_personal=True)

    except Exception as e:
        print(f"Error in inline_query_handler: {e}")
