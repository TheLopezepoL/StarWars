########################################
# Integrantes: Sebastián López Herrera y Daniel Sequeira Retana
# Fecha creación: 26/04/2019 12:00
# Ultima actualización: 26/04/2019 19:20
# Version 0.1 - Pyhton 3.7.3
########################################
# Importación de Librerias
import requests
import json


# Definición de Funciones
def verificarRed():
    urls = ['https://www.google.co.cr/', 'https://www.tec.ac.cr/', 'https://www.python.org/']
    resul = 0
    for url in urls:
        try:
            requests.get(url)
            resul += 1
        except:
            resul -= 1
    if resul > 0:
        return True
    return False


def sacarFrases(pcan):
    url = 'http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote'
    frases = []
    while pcan > 0:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            frases.append(json.loads(respuesta.content.decode('utf-8')))
        else:
            frases.append('Error de conexion; la API no respondio')
        pcan -= 1
    return frases

# Programa Principal


# - FIN - #
