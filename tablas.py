import sqlite3
import pandas as pd
import json

def create_table_users():
    cur = con.cursor()
    f = open('data/users.json', 'r')
    data_users = json.load(f)

    cur.execute("CREATE TABLE IF NOT EXISTS users ("
                "username TEXT PRIMARY KEY,"
                "tel_number TEXT,"
                "hash_password TEXT,"
                "province TEXT,"
                "permission TEXT,"
                "emails_total INTEGER,"
                "emails_phising INTEGER,"
                "emails_clicked INTEGER"
                ");")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS dates_ip("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "ip TEXT,"
                "fecha TEXT,"
                "user_id TEXT,"
                "FOREIGN KEY (user_id) REFERENCES users(username)"
                ");")
    con.commit()

    for elem in data_users["usuarios"]:
        clave = list(elem.keys())[0]

        cur.execute(
            "INSERT OR IGNORE INTO users (username, tel_number, hash_password, province, permission, emails_total, emails_phising, emails_clicked)" \
            "VALUES ('%s','%s','%s','%s','%s', '%d', '%d', '%d')" %
            (clave, elem[clave]['telefono'], elem[clave]['contrasena'],
             elem[clave]['provincia'], elem[clave]['permisos'], int(elem[clave]['emails']['total']),
             int(elem[clave]['emails']['phishing']), int(elem[clave]['emails']['cliclados'])))
        con.commit()
        dates = elem[clave]["fechas"]
        ips = elem[clave]["ips"]
        for date,ip in zip(dates,ips):
            cur.execute("INSERT OR IGNORE INTO dates_ip (ip,fecha,user_id)" \
                        "VALUES ('%s', '%s','%s')" %
                        (ip,date,clave))
            con.commit()




def create_table_legal():
    cur = con.cursor()
    f = open('data/legal.json', 'r')
    data_legal = json.load(f)

    cur.execute("CREATE TABLE IF NOT EXISTS legal ("
                "web_URL TEXT PRIMARY KEY,"
                "cookies INTEGER,"
                "warning INTEGER,"
                "data_protection INTEGER,"
                "creation INTEGER"
                ");")
    con.commit()

    for elem in data_legal["legal"]:
        clave = list(elem.keys())[0]

        cur.execute(
            "INSERT OR IGNORE INTO legal (web_URL, cookies, warning, data_protection, creation)" \
            "VALUES ('%s','%d','%d','%d','%d')" %
            (clave, int(elem[clave]['cookies']), int(elem[clave]['aviso']),
             int(elem[clave]['proteccion_de_datos']), int(elem[clave]['creacion'])))






#conexion a la BBDD
con = sqlite3.connect('bbdd.db')

#crear tabla users
create_table_users()

#crear tabla legal
create_table_legal()

con.commit()
con.close()
