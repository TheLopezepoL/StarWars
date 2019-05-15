########################################
# Integrantes: Sebastián López Herrera y Daniel Sequeira Retana
# Fecha creación: 26/04/2019 12:00
# Ultima actualización: 14/05/2019 23:00
# Version 0.1 - Python 3.7.3
########################################
# Importación de Librerias
import requests
import json
from tkinter import *
# Variable Global
pfrases = []

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
    global pfrases
    url = 'http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote'
    while pcan > 0:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            try:
                pfrases.append(json.loads(respuesta.content.decode('utf-8')))
            except:
                pfrases.append({'id': 0, 'starWarsQuote': 'Error de conexion; la API no respondio - ERROR', 'faction': 0
                                })
        else:
            pfrases.append({'id': 0, 'starWarsQuote': 'Error de conexion; la API no respondio - ERROR', 'faction': 0})
        pcan -= 1
    return pfrases


def sacarNombre():
    global pfrases
    for frase in pfrases:
        texto = frase['starWarsQuote']
        if re.search(' — ', texto):
            texto = texto.split(' — ')
        elif re.search(' - ', texto):
            texto = texto.split(' - ')
        else:
            texto = texto.split(' ? ')
        texto = auxSacarNombre(texto)
        if re.search(" \(", texto[1]):
            texto[1] = texto[1].split(' (')
            texto[1] = texto[1][0]
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


def eliminarFRep():
    global pfrases
    cont = 0
    while cont < len(pfrases)-1:
        f = pfrases[cont]['id']
        cont2 = len(pfrases) - 1
        while cont2 > cont:
            c = pfrases[cont2]['id']
            if f == c:
                pfrases.pop(cont2)
            cont2 -= 1
        cont += 1
    return pfrases


def crearCdA():
    global pfrases
    ncod = len(pfrases)
    pfrases.reverse()
    for p in pfrases:
        nom = p['nom'].upper()
        li = nom[0]
        lf = nom[len(nom)-1]
        cod = li + str(ncod).zfill(3) + '-' + lf
        p['cod'] = cod
        ncod -= 1
    pfrases.reverse()
    return pfrases


def auxCrearMatriz(pcan):
    global pfrases
    pfrases = sacarFrases(pcan)
    pfrases = eliminarFRep()
    pfrases = sacarNombre()
    pfrases = crearCdA()
    frases = pfrases
    return frases


def crearMatriz(pcan):
    global pfrases
    matriz = []
    nom = ''
    cont = 0
    frases = auxCrearMatriz(pcan)
    print(pfrases)
    while len(frases) != 0:
        f = frases[cont]
        CdA = f['cod']
        lis = []
        lfra = []
        lid = []
        nom = f['nom']
        cont2 = 0
        while cont2 <= len(frases)-1:
            i = frases[cont2]
            if i['nom'] == nom:
                lfra.append(i['starWarsQuote'])
                lid.append(i['id'])
                frases.pop(cont2)
                cont2 -= 1
            cont2 += 1
        lis = [nom, lfra, lid, CdA]
        matriz.append(lis)
    print(pfrases)
    return matriz


def crearDict(pmatriz):
    diccfrases = {}
    for per in pmatriz:
        cod = per[3]
        diccfrases[cod] = len(per[2])
    return diccfrases


def sacarMayor(pdict, pmatriz):
    nom = ''
    gcod = ''
    gnum = 0
    for d in pdict:
        val = pdict[d]
        if val > gnum:
            gcod = d
            gnum = val
    for m in pmatriz:
        if m[3] == gcod:
            nom = m[0]
            return 'Más Citado: ' + nom
    return 'Más Citado: ' + nom


def auxllamarFBus(pnum):
    try:
        pnum = int(pnum)
        return True, pnum
    except ValueError:
        return False, pnum


# - FIN - #
