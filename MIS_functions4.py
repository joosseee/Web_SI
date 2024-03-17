import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import stats_script
import base64
from io import BytesIO


def calcular_media_diferencias(df):
    df['fecha'] = pd.to_datetime(df['fecha'], format="%d/%m/%Y")
    df = df.sort_values(by=['user_id', 'fecha'])
    df['diferencia'] = df.groupby('user_id')['fecha'].diff().dt.days
    media = df.groupby('user_id')['diferencia'].mean().dropna()

    media_df = media.reset_index()
    media_df.columns = ['username', 'media']
    return media_df


def plot_to_base64(plot):
    buf = BytesIO()
    plot.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return image_base64


def meanPasswords():
    conn = sqlite3.connect("bbdd.db")
    sql_query_users = "SELECT dates_ip.fecha, dates_ip.user_id FROM dates_ip JOIN users ON dates_ip.user_id = users.username WHERE users.permission = 0"
    sql_query_admins = "SELECT dates_ip.fecha, dates_ip.user_id FROM dates_ip JOIN users ON dates_ip.user_id = users.username WHERE users.permission = 1"

    users_df = pd.read_sql_query(sql_query_users, conn)
    admins_df = pd.read_sql_query(sql_query_admins, conn)

    media_users = calcular_media_diferencias(users_df)
    media_admins = calcular_media_diferencias(admins_df)

    plt.figure()
    media_users.plot(kind='bar', x='username', y='media', legend=False)
    plt.title('Media de tiempo entre cambios de contraseña (Usuarios)', pad=20)
    plt.xlabel('Nombre de usuario', labelpad=20)
    plt.ylabel('Media de Tiempo (días)', labelpad=20)
    plt.xticks(rotation=80)
    plt.tight_layout()
    user_img = plot_to_base64(plt)
    plt.close()

    plt.figure()
    media_admins.plot(kind='bar', x='username', y='media', legend=False)
    plt.title('Media de tiempo entre cambios de contraseña (Administradores)', pad=20)
    plt.xlabel('Nombre de usuario', labelpad=20)
    plt.ylabel('Media de Tiempo (días)', labelpad=20)
    plt.xticks(rotation=80)
    plt.tight_layout()
    admin_img = plot_to_base64(plt)
    plt.close()

    conn.close()

    return user_img, admin_img


def tenUSERS():
    conn = sqlite3.connect('bbdd.db')

    usuarios_df = pd.read_sql_query("SELECT username, hash_password, emails_clicked, emails_phising FROM users", conn)

    hashes_small_rock_you = stats_script.hashear_contraseñas_archivo('SmallRockYou.txt')
    usuarios_df['strength'] = stats_script.comparar_hashes(usuarios_df['hash_password'], hashes_small_rock_you)

    # Calcular la probabilidad de hacer clic en un correo de phishing para cada usuario
    usuarios_df['click_ratio'] = round((usuarios_df['emails_clicked'] / usuarios_df['emails_phising']) * 100, 2)

    # Seleccionar usuarios con contraseñas débiles
    usuarios_debil = usuarios_df[usuarios_df['strength'] == 0]

    usuarios_debil_ordenado = usuarios_debil.sort_values(by='click_ratio', ascending=False)

    # Seleccionar los 10 usuarios con mayor probabilidad de clic en correos de phishing
    top10 = usuarios_debil_ordenado.head(10)

    usuarios_criticos_df = top10[['username', 'click_ratio']].copy()

    # Graficar los usuarios más críticos en un gráfico de barras
    plt.figure()
    usuarios_criticos_df.plot(kind='bar', x='username', y='click_ratio', legend=False)
    plt.title('Top 10 usuarios más críticos', pad=20)
    plt.xlabel('Nombre de usuario', labelpad=20)
    plt.ylabel('Probabilidad de pulsar correo phishing', labelpad=20)
    plt.xticks(rotation=80)
    plt.tight_layout()
    usuarios_criticos_img = plot_to_base64(plt)
    plt.close()

    conn.close()

    return usuarios_criticos_df.to_json(orient="records")


def paginas_desactualizadas():

    conn = sqlite3.connect('bbdd.db')

    # Leer los datos en un DataFrame de Pandas
    df = pd.read_sql_query("SELECT web_URL, cookies, warning, data_protection,creation FROM legal", conn)

    # Convertir la columna de fecha de creación a tipo datetime
    df['creation'] = pd.to_datetime(df['creation'])

    # Calcular el total de políticas para cada página web
    df['total_politicas'] = df['cookies'] + df['warning'] + df['data_protection']

    # Ordenar las páginas web por fecha de creación
    df = df.sort_values(by='creation')

    # Seleccionar las 5 fechas más antiguas entre aquellas que tienen más políticas
    paginas_top5 = df.nlargest(5, 'total_politicas').nsmallest(5, 'creation')

    # Graficar las páginas web en un gráfico de barras
    #paginas_top5.plot(kind='bar', x='Web', y=['Cookies', 'Aviso', 'Protección de datos'], stacked=True)
    #plt.title('Páginas web con más políticas desactualizadas (5 fechas más antiguas)')
    #plt.xlabel('Página web')
    #plt.ylabel('Cantidad de políticas')
    #plt.show()

    # Cerrar la conexión a la base de datos
    conn.close()

    return paginas_top5.to_json(orient="records")


def webs_politicas_privacidad_por_año():

    conn = sqlite3.connect('bbdd.db')

    # Consulta SQL para webs que cumplen todas las políticas de privacidad por año de creación
    sql_query_cumplen = """
          SELECT creation AS Año_Creación,
                 COUNT(*) AS Total_Webs_Cumplen
          FROM legal
          WHERE (cookies + warning + data_protection) = 3
          GROUP BY Año_Creación
      """

    # Consulta SQL para webs que no cumplen todas las políticas de privacidad por año de creación
    sql_query_no_cumplen = """
          SELECT creation AS Año_Creación,
                 COUNT(*) AS Total_Webs_No_Cumplen
          FROM legal
          WHERE (cookies + warning + data_protection) != 3
          GROUP BY Año_Creación
      """

    df_cumplen = pd.read_sql_query(sql_query_cumplen, conn)
    df_no_cumplen = pd.read_sql_query(sql_query_no_cumplen, conn)
    df_comparacion = pd.concat([df_cumplen.set_index('Año_Creación'), df_no_cumplen.set_index('Año_Creación')], axis=1,keys=['Cumplen', 'No_Cumplen']).reset_index()
    df_comparacion.columns = df_comparacion.columns.droplevel(1)
    df_comparacion.fillna(0, inplace=True)
    df_comparacion['Cumplen'] = df_comparacion['Cumplen'].astype(int)
    df_comparacion['No_Cumplen'] = df_comparacion['No_Cumplen'].astype(int)
    df_comparacion.sort_values(by='Año_Creación', inplace=True)

    # Graficar los resultados
    #df.plot(kind='bar', x='Año_Creación', y=['Cumplen_Todas', 'No_Cumplen_Todas'], stacked=True)
    #plt.title('Sitios web que cumplen todas las políticas de privacidad por año de creación')
    #plt.xlabel('Año de Creación')
    #plt.ylabel('Cantidad de Sitios Web')
    #plt.legend(['Cumplen Todas las Políticas', 'No Cumplen Todas las Políticas'])
    #plt.show()
    conn.close()
    return df_comparacion.to_json(orient="records")


paginas_top5 = paginas_desactualizadas()
useres = tenUSERS()
passw = meanPasswords()
webs = webs_politicas_privacidad_por_año()

#print(webs)
#print(paginas_top5)
#print(useres)
#print(passw)
