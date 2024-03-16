#Mostrar la media de tiempo entre las contraseñas
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import stats
def meanPasswords():
    conn = sqlite3.connect("bbdd.db")

    sql_query = "SELECT fecha,user_id FROM dates_ip"



    df = pd.read_sql_query(sql_query,conn)
    df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y')
    # Calcular la diferencia de tiempo para usuarios normales
    usuarios_normales = df[df['user_id'] != 'administrador'].copy()
    usuarios_normales['diferencia_tiempo'] = usuarios_normales.groupby('user_id')['fecha'].transform( lambda x: (x.max() - x.min()).days) / 365
    # Calcular la diferencia de tiempo para administradores
    usuarios_administradores = df[df['user_id'] == 'administrador'].copy()
    usuarios_administradores['diferencia_tiempo'] = usuarios_administradores.groupby('user_id')['fecha'].transform(lambda x: (x.max() - x.min()).days) / 365


    media_tiempo_normales = usuarios_normales['diferencia_tiempo'].mean().astype(int)
    media_tiempo_administradores = usuarios_administradores['diferencia_tiempo'].mean().astype(int)


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
    df_comparacion = pd.concat([df_cumplen.set_index('Año_Creación'), df_no_cumplen.set_index('Año_Creación')], axis=1,keys=['Cumplen', 'No Cumplen']).reset_index()
    df_comparacion.columns = df_comparacion.columns.droplevel(1)
    df_comparacion.fillna(0, inplace=True)
    df_comparacion['Cumplen'] = df_comparacion['Cumplen'].astype(int)
    df_comparacion['No Cumplen'] = df_comparacion['No Cumplen'].astype(int)

    # Graficar los resultados
    #df.plot(kind='bar', x='Año_Creación', y=['Cumplen_Todas', 'No_Cumplen_Todas'], stacked=True)
    #plt.title('Sitios web que cumplen todas las políticas de privacidad por año de creación')
    #plt.xlabel('Año de Creación')
    #plt.ylabel('Cantidad de Sitios Web')
    #plt.legend(['Cumplen Todas las Políticas', 'No Cumplen Todas las Políticas'])
    #plt.show()
    conn.close()
    return df_comparacion



paginas_top5 = paginas_desactualizadas()
useres = tenUSERS()
passw = meanPasswords()
webs = webs_politicas_privacidad_por_año()

print(webs)
print(paginas_top5)
print(useres)
print(passw)


