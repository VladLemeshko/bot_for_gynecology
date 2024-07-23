from aiogram.dispatcher.filters.state import State, StatesGroup

class ItemAddStates(StatesGroup):
    add_short_name_state = State()
    add_full_name_state = State()
    add_keywords_state = State()
    add_pdf_state = State()
