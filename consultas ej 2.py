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

#media y desviacion estandar del total de IPs que se han detectado
print("Media y desviacion estandar del total de IPs que se han detectado")
print("Media:")
print(df_dates.groupby('user_id').count().mean()['ip'])
print("Desviacion estandar:")
print(df_dates.groupby('user_id').count().std()['ip'])

#media y desviacion estandar del numero de emails recibidos de phising en los que ha interactuado cualquier usuario
print("Media y desviación estándar del número de email recibidos de phishing en los que ha interactuado cualquier usuario")
print("Media:")
print(df_users['emails_phising'].mean())
print(("Desviacion estandar:"))
print(df_users['emails_phising'].std())

#valor minimo y valor maximo del total de emails recibidos
print("Valor minimo y valor maximo del total de emials recibidos")
print("Minimo:")
print(df_users['emails_total'].min())
print("Maximo:")
print(df_users['emails_total'].max())

#valor minimo y valor maximo del numero de emails phising en los que ha interactuado un administrador
print("Valor mínimo y valor máximo del número de emails phishing en los que ha interactuado un administrador")
print("Minimo:")
print(df_admin['emails_clicked'].min())
print("Maximo:")
print(df_admin['emails_clicked'].max())