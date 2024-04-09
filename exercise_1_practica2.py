import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import exercise_3
import exercise_4
import base64
from io import BytesIO


def plot_to_base64(plot):
    buf = BytesIO()
    plot.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return image_base64


def xUsers(num_users):
    conn = sqlite3.connect('bbdd.db')

    usuarios_df = pd.read_sql_query("SELECT username, hash_password, emails_clicked, emails_phising FROM users", conn)

    hashes_small_rock_you = exercise_3.hashear_contraseñas_archivo('data/SmallRockYou.txt')
    usuarios_df['strength'] = exercise_3.comparar_hashes(usuarios_df['hash_password'], hashes_small_rock_you)

    # Calcular la probabilidad de hacer clic en un correo de phishing para cada usuario
    usuarios_df['click_ratio'] = round((usuarios_df['emails_clicked'] / usuarios_df['emails_phising']) * 100, 2)

    # Seleccionar usuarios con contraseñas débiles
    usuarios_debil = usuarios_df[usuarios_df['strength'] == 0]
    num_critical = len(usuarios_debil)
    usuarios_debil_ordenado = usuarios_debil.sort_values(by='click_ratio', ascending=False)

    topX = usuarios_debil_ordenado.head(num_users)
    usuarios_criticos_df = topX[['username', 'click_ratio']].copy()

    # Graficar los usuarios más críticos en un gráfico de barras
    plt.figure()
    usuarios_criticos_df.plot(kind='bar', x='username', y='click_ratio', legend=False)
    plt.xlabel('Nombre de usuario', labelpad=20)
    plt.ylabel('Probabilidad de pulsar correo phishing (%)', labelpad=20)
    plt.xticks(rotation=80)
    plt.tight_layout()
    usuarios_criticos_img = plot_to_base64(plt)
    plt.close()

    conn.close()

    return usuarios_criticos_img, num_critical


def xPages():
    # por hacer
    print("hello")
