import sqlite3
import hashlib
import pandas as pd


pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def stats_function():

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('bbdd.db')

    emails_phishing_df = pd.read_sql_query("SELECT permission, emails_phising FROM users", conn)
    passwords_df = pd.read_sql_query("SELECT hash_password, emails_phising FROM users", conn)

    hashes_small_rock_you = hashear_contraseñas_archivo('SmallRockYou.txt')

    passwords_df['strength'] = comparar_hashes(passwords_df['hash_password'], hashes_small_rock_you)

    emails_phishing_df['permission'] = emails_phishing_df['permission'].astype(int)

    # Marcar con 1 los valores ausentes (nulos) y con 0 los valores presentes
    emails_phishing_df['missing'] = emails_phishing_df['emails_phising'].isnull().astype(int)
    passwords_df['missing'] = passwords_df['emails_phising'].isnull().astype(int)

    # Calcular la suma de valores nulos por grupo de 'permission'
    missing_values = emails_phishing_df.groupby('permission')['missing'].sum()
    missing_values_password = passwords_df.groupby('strength')['missing'].sum()

    # Agrupar por 'permission' y calcular las estadísticas y los valores ausentes simultáneamente
    stats_df = emails_phishing_df.groupby('permission')['emails_phising'].agg(['count', 'median', 'mean', 'var', 'max', 'min']).rename(columns={
        'count': 'Número de observaciones',
        'median': 'Mediana',
        'mean': 'Media',
        'var': 'Varianza',
        'max': 'Máximo',
        'min': 'Mínimo',
    })

    passwords_df = passwords_df.groupby('strength')['emails_phising'].agg(['count', 'median', 'mean', 'var', 'max', 'min']).rename(columns={
        'count': 'Número de observaciones',
        'median': 'Mediana',
        'mean': 'Media',
        'var': 'Varianza',
        'max': 'Máximo',
        'min': 'Mínimo',
    })

    # Asegurarse de que el índice de missing_values coincide con el de stats_df
    stats_df['Número de valores ausentes (missing)'] = missing_values

    passwords_df['Número de valores ausentes (missing)'] = missing_values_password

    stats_df = stats_df[['Número de observaciones', 'Número de valores ausentes (missing)', 'Mediana', 'Media', 'Varianza', 'Máximo', 'Mínimo']]
    passwords_df = passwords_df[['Número de observaciones', 'Número de valores ausentes (missing)', 'Mediana', 'Media', 'Varianza', 'Máximo', 'Mínimo']]

    stats_df = stats_df.rename(index={0: 'Usuario', 1: 'Administrador'})
    stats_df = stats_df.rename_axis("Tipo de Permiso", axis='index')

    stats_df = stats_df.round(4)

    passwords_df = passwords_df.rename(index={0: 'Débil', 1: 'Fuerte'})
    passwords_df = passwords_df.rename_axis("Fuerza de Contraseña", axis='index')

    passwords_df = passwords_df.round(4)

    conn.close()

    return stats_df, passwords_df


def hashear_contraseñas_archivo(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        passwords = archivo.read().splitlines()
        hashes = set(hashlib.md5(passwd.encode()).hexdigest() for passwd in passwords)
    return hashes


def comparar_hashes(hashes_base_datos, hashes_diccionario):
    list = []

    for i in hashes_base_datos:
        if i in hashes_diccionario:
            list.append(0)
        else:
            list.append(1)

    return list
