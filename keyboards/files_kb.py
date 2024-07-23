from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_files_kb() -> InlineKeyboardMarkup:
    kb_menu = InlineKeyboardMarkup(row_width=2)
    
    kb_menu.add(InlineKeyboardButton("Анкеты 📄", switch_inline_query_current_chat="Анкеты"))
    kb_menu.insert(InlineKeyboardButton("Шкалы ⚖", switch_inline_query_current_chat="Шкалы"))
    kb_menu.add(InlineKeyboardButton("Показания 📋", switch_inline_query_current_chat="Показания"))
    kb_menu.add(InlineKeyboardButton("Критерии оценки качества 📐", switch_inline_query_current_chat="Критерии оценки качества"))
    kb_menu.add(InlineKeyboardButton("Поиск🔎", switch_inline_query_current_chat=""))
    
    return kb_menu