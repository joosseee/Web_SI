import pandas as pd
import numpy as np
import sqlite3
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from joblib import dump


# Función para guardar o reemplazar el modelo de Regresión Lineal
def save_model(model):
    path = 'data/modelo_regresion_lineal.joblib'

    if os.path.exists(path):
        os.remove(path)

    dump(model, path)


# Abrir conexión base de datos
conn = sqlite3.connect('data/bbdd.db')


# Consultar la base de datos para obtener los datos de los usuarios
query = "SELECT * FROM users"
df_users = pd.read_sql(query, conn)


# Cerrar conexión base de datos
conn.close()


# Calcular la probabilidad de pulsar correo de spam, manejando la división por cero
df_users['prob_click_spam'] = df_users['emails_clicked'] / df_users['emails_phising'].replace(0, np.nan)


# Llenar los valores NaN resultantes de la división por cero con 0
df_users['prob_click_spam'] = df_users['prob_click_spam'].fillna(0)


# Cargar el archivo JSON para extraer el estado crítico de cada usuario
with open('data/users_data_online_clasificado.json', 'r') as file:
    json_data = json.load(file)


# Extraer el estado crítico de cada usuario
critico_info = {}
for user_dict in json_data['usuarios']:
    for username, info in user_dict.items():
        critico_info[username] = info['critico']


# Añadir la columna 'critico' al DataFrame de usuarios
df_users['critico'] = df_users['username'].apply(lambda x: critico_info.get(x, 0))


# Seleccionar las características y la variable objetivo
X = df_users[['prob_click_spam']]
y = df_users['critico']


# Dividir los datos en conjuntos de entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Modelo de Regresión Lineal
modelo = LinearRegression()


# Entrenar el modelo
modelo.fit(x_train, y_train)


# Hacer predicciones con el conjunto de prueba
y_pred = modelo.predict(x_test)


# Guardar el modelo de Regresión Lineal
save_model(modelo)
