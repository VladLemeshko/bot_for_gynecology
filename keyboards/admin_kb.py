from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_admin_keyboard():
    kb_admin_panel = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton("Анкета")],
                    [KeyboardButton("Шкала")],
                    [KeyboardButton("Показание")],
                    [KeyboardButton("Критерий оценки качества")]
                    ], resize_keyboard=True)
    
    return kb_admin_panel

def get_adminmode_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("Панель администратора")]],
        resize_keyboard=True)