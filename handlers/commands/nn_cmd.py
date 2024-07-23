from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from keyboards.menu_kb import create_menu_kb
from handlers.commands.menu import create_menu_kb
from NN.health_risk import predict_health_risk  # Импортируем функцию предсказания здоровья

# Создаем класс состояний для использования State machine
class NeuralNetworkQuestions(StatesGroup):
    waiting_for_age = State()
    waiting_for_systolic_bp = State()
    waiting_for_diastolic_bp = State()
    waiting_for_bs = State()
    waiting_for_body_temp = State()
    waiting_for_heart_rate = State()
    waiting_for_result = State()

# Обработчик для нажатия на кнопку "Нейронная сеть"
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'nn', state="*")
async def neural_network_button_handler(callback_query: types.CallbackQuery, state: FSMContext):
    # Устанавливаем состояние "waiting_for_age" для начала задания вопросов
    await NeuralNetworkQuestions.waiting_for_age.set()
    
    # Отправляем первый вопрос пользователю
    await callback_query.message.answer("Какой ваш возраст?")



# Обработчик для ответа на вопрос о возрасте
@dp.message_handler(state=NeuralNetworkQuestions.waiting_for_age)
async def answer_age(message: types.Message, state: FSMContext):
    # Получаем ответ пользователя
    age = message.text
    
    # Сохраняем ответ в контексте состояния
    await state.update_data(age=age)
    
    # Задаем следующий вопрос
    await NeuralNetworkQuestions.next()
    await message.answer("Какое ваше значение артериального давления (верхнее)?")

# Обработчик для ответа на вопрос о верхнем артериальном давлении (Systolic BP)
@dp.message_handler(state=NeuralNetworkQuestions.waiting_for_systolic_bp)
async def answer_systolic_bp(message: types.Message, state: FSMContext):
    # Получаем ответ пользователя
    systolic_bp = message.text
    
    # Сохраняем ответ в контексте состояния
    await state.update_data(systolic_bp=systolic_bp)
    
    # Задаем следующий вопрос
    await NeuralNetworkQuestions.next()
    await message.answer("Какое ваше значение артериального давления (нижнее)?")

# Обработчик для ответа на вопрос о нижнем артериальном давлении (Diastolic BP)
@dp.message_handler(state=NeuralNetworkQuestions.waiting_for_diastolic_bp)
async def answer_diastolic_bp(message: types.Message, state: FSMContext):
    # Получаем ответ пользователя
    diastolic_bp = message.text
    
    # Сохраняем ответ в контексте состояния
    await state.update_data(diastolic_bp=diastolic_bp)
    
    # Задаем следующий вопрос
    await NeuralNetworkQuestions.next()
    await message.answer("Какое ваше значение уровня сахара в крови (BS)?")

# Обработчик для ответа на вопрос о уровне сахара в крови (BS)
@dp.message_handler(state=NeuralNetworkQuestions.waiting_for_bs)
async def answer_bs(message: types.Message, state: FSMContext):
    # Получаем ответ пользователя
    bs = message.text
    
    # Сохраняем ответ в контексте состояния
    await state.update_data(bs=bs)
    
    # Задаем следующий вопрос
    await NeuralNetworkQuestions.next()
    await message.answer("Какое ваше значение температуры тела (Body Temperature)?")

# Обработчик для ответа на вопрос о температуре тела (Body Temperature)
@dp.message_handler(state=NeuralNetworkQuestions.waiting_for_body_temp)
async def answer_body_temp(message: types.Message, state: FSMContext):
    # Получаем ответ пользователя
    body_temp_celsius = float(message.text)
    
    # Конвертируем температуру из градусов Цельсия в градусы Фаренгейта
    body_temp_fahrenheit = (9 / 5) * body_temp_celsius + 32
    
    # Сохраняем ответ в контексте состояния
    await state.update_data(body_temp=body_temp_fahrenheit)
    
    # Задаем следующий вопрос
    await NeuralNetworkQuestions.next()
    await message.answer("Какое ваше значение пульса (Heart Rate)?")

# Обработчик для ответа на вопрос о пульсе (Heart Rate)
@dp.message_handler(state=NeuralNetworkQuestions.waiting_for_heart_rate)
async def answer_heart_rate(message: types.Message, state: FSMContext):
    # Получаем ответ пользователя
    heart_rate = float(message.text)
    
    # Сохраняем ответ в контексте состояния
    await state.update_data(heart_rate=heart_rate)
    
    # Получаем данные из контекста состояния
    user_data = await state.get_data()
    
    # Получаем данные о пользователе из контекста
    user_id = message.from_user.id
    age = user_data['age']
    systolic_bp = user_data['systolic_bp']
    diastolic_bp = user_data['diastolic_bp']
    bs = user_data['bs']
    body_temp = user_data['body_temp']
    heart_rate = user_data['heart_rate']
    
    # Получаем результат работы нейронной сети
    result = await predict_health_risk(user_id, age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate)
    
    # Конвертируем результат на русский язык
    if result == "High Risk":
        result_russian = "Высокий риск"
    elif result == "Mid Risk":
        result_russian = "Средний риск"
    else:
        result_russian = "Низкий риск"
    
    # Отправляем результат пользователю
    await message.answer(f"Результат работы нейронной сети: {result_russian}")
    
    # Завершаем состояние
    await state.finish()
