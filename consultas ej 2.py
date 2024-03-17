import sqlite3
import pandas as pd

con = sqlite3.connect('bbdd.db')

#consultas
q_users = "SELECT * FROM users WHERE username IS NOT NULL"
q_fechas = "SELECT * FROM dates_ip WHERE user_id IN(SELECT username FROM users)"
q_admin = "SELECT * FROM users WHERE permission IS 1"

#dataframes
df_users = pd.read_sql_query(q_users, con)
df_dates = pd.read_sql_query(q_fechas, con)
df_admin = pd.read_sql_query(q_admin, con)

#número de muestras
print("Numero de muestras:")
print(df_users['username'].count(), end="\n")

#media y desviación estándar del total de fechas en las que se ha cambiado la contraseña
print("Media y desviacion estandar del total de fechas en las que se ha cambiado la contraseña")
print("Media:")
print(df_dates.groupby('user_id').count().mean()['fecha'])
print("Desviacion estandar:")
print(df_dates.groupby('user_id').count().std()['fecha'])