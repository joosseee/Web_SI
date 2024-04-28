import pandas as pd
import numpy as np
import sqlite3
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from joblib import dump


# Función para guardar o reemplazar el modelo de Regresión Lineal
def save_model(model, path):
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


# Calcular la proporción de emails de phishing sobre el total
df_users['phishing_ratio'] = df_users['emails_phising'] / df_users['emails_total'].replace(0, np.nan)


# Llenar los valores NaN resultantes de la división por cero con 0
df_users['phishing_ratio'] = df_users['phishing_ratio'].fillna(0)


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


# Seleccionar las características (proporción de emails phishing | probabilidad de click phishing | permiso) y la variable objetivo (criticidad)
X = df_users[['phishing_ratio', 'prob_click_spam', 'permission']]
y = df_users['critico']


# Dividir los datos en conjuntos de entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Modelo de Regresión Lineal
modelo = LinearRegression()
modeloRandomForest = RandomForestRegressor()
#Modelo de Árbol de Decisión
modeloDecisionTree = DecisionTreeRegressor()

# Entrenar los modelos
modelo.fit(x_train, y_train)
modeloRandomForest.fit(x_train,y_train)
modeloDecisionTree.fit(x_train,y_train)


# Hacer predicciones con el conjunto de prueba
y_pred = modelo.predict(x_test)
y_pred_randomForest = modeloRandomForest.predict(x_test)
y_pred_decisionTree = modeloDecisionTree.predict(x_test)

# Guardar el modelo de Regresión Lineal
save_model(modelo, 'data/modelo_regresion_lineal.joblib')
save_model(modeloRandomForest, 'data/modelo_random_forest.joblib')
save_model(modeloDecisionTree, 'data/modelo_decision_tree.joblib')
