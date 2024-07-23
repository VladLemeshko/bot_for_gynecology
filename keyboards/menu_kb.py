from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_menu_kb() -> InlineKeyboardMarkup:
    kb_menu = InlineKeyboardMarkup(row_width=2)
    
    kb_menu.add(InlineKeyboardButton("Файлы 📁", callback_data='files'))
    kb_menu.add(InlineKeyboardButton("Калькуляторы 🧮", callback_data='calculators'))
    kb_menu.add(InlineKeyboardButton("Нейронная сеть 🧠", callback_data='nn'))
    
    return kb_menu