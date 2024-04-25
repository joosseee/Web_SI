import sqlite3
import pandas as pd


def data_querys():
    con = sqlite3.connect('data/bbdd.db')


    # consultas
    q_users = "SELECT * FROM users WHERE username IS NOT NULL"
    q_fechas = "SELECT * FROM dates_ip"
    q_admin = "SELECT * FROM users WHERE permission IS 1"


    # dataframes
    df_users = pd.read_sql_query(q_users, con)
    df_dates = pd.read_sql_query(q_fechas, con)
    df_admin = pd.read_sql_query(q_admin, con)


    results = {
        'numero_muestras': df_users['username'].count(),
        'media_fechas': round(df_dates.groupby('user_id').count().mean()['fecha'], 4),
        'desviacion_fechas': round(df_dates.groupby('user_id').count().std()['fecha'], 4),
        'media_ip': round(df_dates.groupby('user_id').count().mean()['ip'], 4),
        'desviacion_ip': round(df_dates.groupby('user_id').count().std()['ip'], 4),
        'media_phishing': round(df_users['emails_clicked'].mean(), 4),
        'desviacion_phishing': round(df_users['emails_clicked'].std(), 4),
        'min_emails': df_users['emails_total'].min(),
        'max_emails': df_users['emails_total'].max(),
        'min_phishing_admin': df_admin['emails_clicked'].min(),
        'max_phishing_admin': df_admin['emails_clicked'].max()
    }

    con.close()

    df_results = pd.DataFrame([results])

    return df_results
