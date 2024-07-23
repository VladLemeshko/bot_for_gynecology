from create_bot import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.calc_kb import create_calculator_kb
from data.users_db import create_query
from aiogram.types import ParseMode
from states.calc_states import CalculatorStates

# Обработчик нажатий на кнопки
@dp.callback_query_handler(lambda c: c.data == 'calculators')
async def process_calculators(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Выберите калькулятор:", reply_markup=create_calculator_kb())

# Обработчик для выбора калькулятора ИМТ
@dp.callback_query_handler(lambda c: c.data == 'calculator_bmi')
async def process_bmi(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите ваш вес в килограммах:")
    await CalculatorStates.waiting_for_weight.set()

# Обработчик ввода веса для ИМТ
@dp.message_handler(state=CalculatorStates.waiting_for_weight, content_types=types.ContentTypes.TEXT)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        await state.update_data(weight=weight)
        await message.answer("Введите ваш рост в метрах (Пример: 1.5):")
        await CalculatorStates.waiting_for_height.set()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное значение веса.")

# Обработчик ввода роста для ИМТ
@dp.message_handler(state=CalculatorStates.waiting_for_height, content_types=types.ContentTypes.TEXT)
async def process_height(message: types.Message, state: FSMContext):
    try:
        height = float(message.text)
        user_data = await state.get_data()
        weight = user_data['weight']
        bmi = weight / (height ** 2)
        if bmi < 18:
            interpretation = "дефицит массы тела"
        elif 18 <= bmi < 25:
            interpretation = "норма"
        elif 25 <= bmi < 30:
            interpretation = "избыточная масса тела"
        elif 30 <= bmi < 35:
            interpretation = "ожирение I степени"
        elif 35 <= bmi < 40:
            interpretation = "ожирение II степени"
        else:
            interpretation = "ожирение III степени"

        result_text = f"Ваш ИМТ: {bmi:.2f} - {interpretation}"

        # Сохранение результата в БД
        user_id = message.from_user.id
        query_data = f"Вес: {weight}, Рост: {height}, ИМТ: {bmi:.2f}"
        await create_query(user_id, query_data)

        await message.answer(result_text, parse_mode=ParseMode.MARKDOWN)
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное значение роста.")

# Обработчик для выбора калькулятора ИСА
@dp.callback_query_handler(lambda c: c.data == 'calculator_androgens')
async def process_androgens(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите общий Тестостерон (нмоль/л):")
    await CalculatorStates.waiting_for_testosterone.set()

@dp.message_handler(state=CalculatorStates.waiting_for_testosterone, content_types=types.ContentTypes.TEXT)
async def process_testosterone(message: types.Message, state: FSMContext):
    try:
        testosterone = float(message.text)
        await state.update_data(testosterone=testosterone)
        await message.answer("Введите Глобулин связывающий половые гормоны (нмоль/л):")
        await CalculatorStates.waiting_for_shbg.set()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное значение тестостерона.")

@dp.message_handler(state=CalculatorStates.waiting_for_shbg, content_types=types.ContentTypes.TEXT)
async def process_shbg(message: types.Message, state: FSMContext):
    try:
        shbg = float(message.text)
        user_data = await state.get_data()
        testosterone = user_data['testosterone']
        isa = (testosterone / shbg) * 100
        interpretation = "Нормальное значение ИСА у женщин репродуктивного периода – 0,8-11%."

        result_text = f"Ваш ИСА: {isa:.2f}%\n{interpretation}"

        # Сохранение результата в БД
        user_id = message.from_user.id
        query_data = f"Общий Тестостерон: {testosterone}, ГСПГ: {shbg}, ИСА: {isa:.2f}%"
        await create_query(user_id, query_data)

        await message.answer(result_text, parse_mode=ParseMode.MARKDOWN)
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное значение ГСПГ.")

# Обработчик для выбора калькулятора Caro
@dp.callback_query_handler(lambda c: c.data == 'calculator_caro')
async def process_caro(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите уровень глюкозы (ммоль/л):")
    await CalculatorStates.waiting_for_glucose.set()

@dp.message_handler(state=CalculatorStates.waiting_for_glucose, content_types=types.ContentTypes.TEXT)
async def process_glucose(message: types.Message, state: FSMContext):
    try:
        glucose = float(message.text)
        await state.update_data(glucose=glucose)
        await message.answer("Введите уровень инсулина (мкМЕ/мл):")
        await CalculatorStates.waiting_for_insulin.set()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное значение глюкозы.")

@dp.message_handler(state=CalculatorStates.waiting_for_insulin, content_types=types.ContentTypes.TEXT)
async def process_insulin(message: types.Message, state: FSMContext):
    try:
        insulin = float(message.text)
        user_data = await state.get_data()
        glucose = user_data['glucose']
        caro = glucose / insulin
        interpretation = "Значения Caro ниже 0,33 свидетельствуют об инсулинорезистентности."

        result_text = f"Ваш индекс Caro: {caro:.2f}\n{interpretation}"

        # Сохранение результата в БД
        user_id = message.from_user.id
        query_data = f"Глюкоза: {glucose}, Инсулин: {insulin}, Caro: {caro:.2f}"
        await create_query(user_id, query_data)

        await message.answer(result_text, parse_mode=ParseMode.MARKDOWN)
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное значение инсулина.")

# Обработчик для выбора калькулятора HOMA-IR
@dp.callback_query_handler(lambda c: c.data == 'calculator_homa_ir')
async def process_homa_ir(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите уровень глюкозы (ммоль/л):")
    await CalculatorStates.waiting_for_homa_glucose.set()

@dp.message_handler(state=CalculatorStates.waiting_for_homa_glucose, content_types=types.ContentTypes.TEXT)
async def process_homa_glucose(message: types.Message, state: FSMContext):
    try:
        glucose = float(message.text)
        await state.update_data(glucose=glucose)
        await message.answer("Введите уровень инсулина (мкМЕ/мл):")
        await CalculatorStates.waiting_for_homa_insulin.set()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное значение глюкозы.")

@dp.message_handler(state=CalculatorStates.waiting_for_homa_insulin, content_types=types.ContentTypes.TEXT)
async def process_homa_insulin(message: types.Message, state: FSMContext):
    try:
        insulin = float(message.text)
        user_data = await state.get_data()
        glucose = user_data['glucose']
        homa_ir = (glucose * insulin) / 22.5
        interpretation = "В норме индекс HOMA не превышает 2,7."

        if homa_ir > 2.7:
            result_text = f"Ваш индекс HOMA-IR: *{homa_ir:.2f}* - превышает норму\n{interpretation}"
        else:
            result_text = f"Ваш индекс HOMA-IR: {homa_ir:.2f}\n{interpretation}"

        # Сохранение результата в БД
        user_id = message.from_user.id
        query_data = f"Глюкоза: {glucose}, Инсулин: {insulin}, HOMA-IR: {homa_ir:.2f}"
        await create_query(user_id, query_data)

        await message.answer(result_text, parse_mode=ParseMode.MARKDOWN)
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное значение инсулина.")

# Обработчик для выбора калькулятора ROMA
@dp.callback_query_handler(lambda c: c.data == 'calculator_roma')
async def process_roma(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Пациентка в постменопаузе? (да/нет):")
    await CalculatorStates.waiting_for_menopause_status.set()

@dp.message_handler(state=CalculatorStates.waiting_for_menopause_status, content_types=types.ContentTypes.TEXT)
async def process_menopause_status(message: types.Message, state: FSMContext):
    try:
        menopause_status = message.text.strip().lower()
        if menopause_status not in ['да', 'нет']:
            raise ValueError("Некорректный ответ")

        await state.update_data(menopause_status=menopause_status)
        await message.answer("Введите уровень СА125:")
        await CalculatorStates.waiting_for_ca125.set()
    except ValueError:
        await message.answer("Пожалуйста, введите 'да' или 'нет'.")

@dp.message_handler(state=CalculatorStates.waiting_for_ca125, content_types=types.ContentTypes.TEXT)
async def process_ca125(message: types.Message, state: FSMContext):
    try:
        ca125 = float(message.text)
        await state.update_data(ca125=ca125)
        await message.answer("Введите уровень НЕ4:")
        await CalculatorStates.waiting_for_he4.set()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное значение СА125.")

@dp.message_handler(state=CalculatorStates.waiting_for_he4, content_types=types.ContentTypes.TEXT)
async def process_he4(message: types.Message, state: FSMContext):
    try:
        he4 = float(message.text)
        user_data = await state.get_data()
        ca125 = user_data['ca125']
        menopause_status = user_data['menopause_status']

        if menopause_status == 'да':
            pi = 8.09 + 1.04 * he4 + 0.732 * ca125
        else:
            pi = 12.0 + 2.38 * he4 + 0.0626 * ca125

        exp_pi = pow(2.71828, pi)
        roma = (exp_pi / (1 + exp_pi)) * 100

        result_text = f"Ваш индекс ROMA: {roma:.2f}%"

        # Сохранение результата в БД
        user_id = message.from_user.id
        query_data = f"СА125: {ca125}, НЕ4: {he4}, ROMA: {roma:.2f}%"
        await create_query(user_id, query_data)

        await message.answer(result_text, parse_mode=ParseMode.MARKDOWN)
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное значение НЕ4.")
