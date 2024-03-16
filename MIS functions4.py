#Mostrar la media de tiempo entre las contraseñas
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import stats
def meanPasswords():
    conn = sqlite3.connect("bbdd.db")

    sql_query = "SELECT fecha,user_id FROM dates_ip"


    df = pd.read_sql_query(sql_query,conn)

    df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)








    usuarios_normales = df[df['user_id'] != 'administrador']
    usuarios_normales['diferencia_tiempo'] = usuarios_normales.groupby('user_id')['fecha'].diff().dt.days

    usuarios_administradores = df[df['user_id']  == 'administrador']
    usuarios_administradores['diferencia_tiempo'] = usuarios_administradores.groupby('user_id')['fecha'].diff().dt.days

    media_tiempo_normales = usuarios_normales['diferencia_tiempo'].mean()
    media_tiempo_administradores = usuarios_administradores['diferencia_tiempo'].mean()


    media_df = pd.DataFrame({
        'Usuarios': ['Normales', 'Administradores'],
        'Media_tiempo': [media_tiempo_normales, media_tiempo_administradores]
    })

    #media_df.plot(kind='bar', x='Usuarios', y='Media_tiempo', legend=False)
    #plt.title('Media de tiempo entre contraseñas')
    #plt.xlabel('Tipo de Usuario')
    #plt.ylabel('Media de Tiempo (días)')
    #plt.show()


    conn.close()

    return media_df


def tenUSERS():
    conn = sqlite3.connect('bbdd.db')

    usuarios_df = pd.read_sql_query("SELECT username, hash_password FROM users", conn)
    correos_phishing_df = pd.read_sql_query("SELECT username, emails_clicked,emails_phising FROM users", conn)


    hashes_small_rock_you = stats.hashear_contraseñas_archivo('SmallRockYou.txt')
    usuarios_df['strength'] = stats.comparar_hashes(usuarios_df['hash_password'], hashes_small_rock_you)

    # Calcular la probabilidad de hacer clic en un correo de phishing para cada usuario
    correos_phishing_df['probabilidad_click'] = correos_phishing_df['emails_clicked'] / correos_phishing_df[
        'emails_phising']

    # Seleccionar usuarios con contraseñas débiles
    usuarios_debil = usuarios_df[usuarios_df['strength'] == 1]

    # Fusionar los DataFrames para obtener los usuarios con contraseñas débiles y su probabilidad de clic
    usuarios_criticos_df = usuarios_debil.merge(correos_phishing_df, on='username')

    # Seleccionar los 10 usuarios con mayor probabilidad de clic en correos de phishing
    usuarios_criticos_top10 = usuarios_criticos_df.nlargest(10, 'probabilidad_click')

    # Graficar los usuarios más críticos en un gráfico de barras
    #usuarios_criticos_top10.plot(kind='bar', x='user_id', y='probabilidad_click', legend=False)
    #plt.title('Usuarios más críticos')
    #plt.xlabel('Usuario')
    #plt.ylabel('Probabilidad de clic en correos de phishing')
    #plt.show()



    conn.close()

    return usuarios_criticos_top10


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

    return paginas_top5


def webs_politicas_privacidad_por_año():

    conn = sqlite3.connect('bbdd.db.db')

    # Consulta SQL para extraer los datos relevantes
    sql_query = """
        SELECT strftime('%Y', creation) AS Año_Creación,
               COUNT(*) AS Total_Webs,
               SUM(cookies + warning + data_protection) AS Cumplen_Todas
        FROM legal
        WHERE (Cookies + Aviso + Protección_de_datos) = 3
        GROUP BY Año_Creación
    """


    df = pd.read_sql_query(sql_query, conn)

    # Calcular la cantidad de sitios web que no cumplen todas las políticas de privacidad
    df['No_Cumplen_Todas'] = df['Total_Webs'] - df['Cumplen_Todas']

    # Graficar los resultados




paginas_top5 = paginas_desactualizadas()
useres = tenUSERS()
passw = meanPasswords()


