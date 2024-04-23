import requests
from datetime import datetime


def format_vulnerabilities(vulnerabilities):
    for vulnerability in vulnerabilities:
        # Formatear las fechas en el formato deseado
        vulnerability['Published'] = format_datetime(vulnerability['Published'])
        vulnerability['Modified'] = format_datetime(vulnerability['Modified'])
    return vulnerabilities


def format_datetime(date_string):
    # Convertir la cadena de fecha a un objeto datetime
    date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    # Formatear la fecha en el formato deseado
    return date_obj.strftime("%d/%m/%Y - %H:%M:%S")


def get_latest_vulnerabilities():
    response = requests.get('https://cve.circl.lu/api/last')
    if response.status_code == 200:
        vulnerabilities = response.json()  # Convertir la respuesta en JSON
        # Formatear las fechas en cada vulnerabilidad
        vulnerabilities = format_vulnerabilities(vulnerabilities)
        return vulnerabilities
    else:
        return None
