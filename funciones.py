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
    resul = []
    for url in urls:
        try:
            requests.get(url)
            resul.append(1)
        except:
            resul.append(0)
    if resul.count(0) < 2:
        return True
    return False




def sacarFrases(pcan):
    frases = []
    while pcan > 0:
        url = 'http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote'
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            contenido = json.loads(respuesta.content.decode('utf-8'))
        else:
            contenido = 'Error de conexion: intente de nuevo'
        frases.append(contenido)
        pcan -= 1
    return frases

# Programa Principal


# - FIN - #
