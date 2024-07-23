from aiogram.dispatcher.filters.state import State, StatesGroup

class CalculatorStates(StatesGroup):
    waiting_for_weight = State()
    waiting_for_height = State()
    waiting_for_testosterone = State()
    waiting_for_shbg = State()
    waiting_for_glucose = State()
    waiting_for_insulin = State()
    waiting_for_homa_glucose = State()
    waiting_for_menopause_status = State()
    waiting_for_ca125 = State()
    waiting_for_he4 = State()
    waiting_for_homa_insulin = State()