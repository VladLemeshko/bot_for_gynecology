import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras import layers
from sklearn.preprocessing import MinMaxScaler
from data.users_db import insert_nn_data

# Указываем путь к файлу CSV
csv_file_path = "data/Maternal Health Risk Data Set.csv"

# Считываем данные из файла CSV в DataFrame
df = pd.read_csv(csv_file_path)

df.drop(index=df[df['HeartRate'] == 7].index, inplace=True)

df['Age'].sort_values().head(10)

df['HighRisk'] = pd.get_dummies(df['RiskLevel'])['high risk'].map({True:1, False:0})
df['MidRisk'] = pd.get_dummies(df['RiskLevel'])['mid risk'].map({True:1, False:0})
df['LowRisk'] =  pd.get_dummies(df['RiskLevel'])['low risk'].map({True:1, False:0})
df.drop(columns=['RiskLevel'], inplace=True)

features = df.drop(columns=['HighRisk', 'MidRisk', 'LowRisk'])
labels = df[['HighRisk', 'MidRisk', 'LowRisk']]
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=1)

scaler = MinMaxScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

model = keras.Sequential([
    layers.Dense(128, input_shape=[6], activation='relu'),
    layers.Dropout(rate=0.3),
    layers.Dense(128, activation='relu'),
    layers.Dropout(rate=0.3),
    layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Добавим обратные вызовы для отслеживания процесса обучения
history = model.fit(X_train, y_train, epochs=500, batch_size=32, verbose=1, 
                    callbacks=[keras.callbacks.EarlyStopping(patience=10), 
                               keras.callbacks.ModelCheckpoint("model_checkpoint.keras", save_best_only=True)])

model.evaluate(X_test, y_test, batch_size=32)

# Инициализация модели нейронной сети при запуске программы
global_model = None

async def initialize_model():
    global global_model
    global_model = model
    return global_model

# Функция для использования нейронной сети и делания предсказания
async def predict_health_risk(user_id, age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate):
    global global_model

    # Предобработка данных, масштабирование и создание DataFrame
    input_data = pd.DataFrame({
        'Age': [age],
        'SystolicBP': [systolic_bp],
        'DiastolicBP': [diastolic_bp],
        'BS': [bs],
        'BodyTemp': [body_temp],
        'HeartRate': [heart_rate]
    })

    # Масштабирование данных
    input_data_scaled = pd.DataFrame(scaler.transform(input_data), columns=input_data.columns)

    # Получение предсказания от модели
    prediction = global_model.predict(input_data_scaled)

    # Преобразование предсказания в текстовый ответ
    risk_levels = ['High Risk', 'Mid Risk', 'Low Risk']
    predicted_risk = risk_levels[np.argmax(prediction)]

    # Сохранение данных пользователя в базе данных
    await insert_nn_data(user_id, age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate, predicted_risk)

    return predicted_risk
