########################################
# Integrantes: Sebastián López Herrera y Daniel Sequeira Retana
# Fecha creación: 26/04/2019 12:00
# Ultima actualización: 26/04/2019 19:20
# Version 0.1 - Python 3.7.3
########################################
# Importación de Librerias
import requests
import json
import re
import ast


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


def sacarNombre(pfrases):
    nombres = []
    for frase in pfrases:
        texto = frase['starWarsQuote']
        if re.search(' — ', texto):
            texto = texto.split(' — ')
        elif re.search(' - ', texto):
            texto = texto.split(' - ')
        else:
            texto = texto.split(' ? ')
        texto = auxSacarNombre(texto)
        frase['nom'] = texto[1]
    return pfrases


def auxSacarNombre(ptexto):
    f = len(ptexto) - 1
    for l in range(1, f):
        ptexto[0] = ptexto[0] + ' - ' + ptexto[l]
    while f > 1:
        ptexto.pop(1)
        f -= 1
    return ptexto


def eliminarFRep(pfrases):
    for n in range(len(pfrases)):
        pfrases[n] = str(pfrases[n])
    pfrases = list(set(pfrases))
    for n in range(len(pfrases)):
        pfrases[n] = ast.literal_eval(pfrases[n])
    return pfrases


def crearCdA(pfrases):
    ncod = len(pfrases)
    pfrases.reverse()
    for p in pfrases:
        ncod += 1
        nom = p['nom'].upper()
        li = nom[0]
        lf = nom[len(nom)-1]
        cod = li + str(ncod).zfill(3) + '-' + lf
        p['cod'] = cod
        ncod -= 1
    pfrases.reverse()
    return pfrases


# Programa Principal
if verificarRed():
    frases = sacarFrases(5)
    frases = eliminarFRep(frases)
    frases = sacarNombre(frases)
    frases = crearCdA(frases)
    print(frases)
else:
    print('Nel we')



# - FIN - #
