from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_calculator_kb() -> InlineKeyboardMarkup:
    kb_calculator = InlineKeyboardMarkup(row_width=1)
    kb_calculator.add(InlineKeyboardButton("Индекс Свободных андрогенов", callback_data='calculator_androgens'))
    kb_calculator.add(InlineKeyboardButton("Индекс массы тела (ИМТ)", callback_data='calculator_bmi'))
    kb_calculator.add(InlineKeyboardButton("Индекс Caro", callback_data='calculator_caro'))
    kb_calculator.add(InlineKeyboardButton("Индекс НОМА-IR", callback_data='calculator_homa_ir'))
    kb_calculator.add(InlineKeyboardButton("Индекс ROMA", callback_data='calculator_roma'))
    return kb_calculator