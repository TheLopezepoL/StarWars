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
import CrearXML
import EnviarBackUp

import os
import xml.etree.ElementTree as et


base_path = os.path.dirname(os.path.realpath(__file__))
xml_file = os.path.join(base_path, "books.xml")
tree = et.parse(xml_file) # lo guarda en memoria
root = tree.getroot()

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
    print(pfrases)
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



def crearMatriz(pcan):
    global pfrases
    matriz = []
    nom = ''
    cont = 0
    frases = sacarFrases(pcan)
    frases = eliminarFRep()
    frases = sacarNombre()
    frases = crearCdA()
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
                CrearXML.crearFrase(str(i["id"]),i['starWarsQuote'],i["nom"],i["cod"])
                frases.pop(cont2)
                cont2 -= 1
            cont2 += 1
        print("nom:", nom, "lfra: ", lfra, "lid: ", lid, "CdA:", CdA)
        lis = [nom, lfra, lid, CdA]
        matriz.append(lis)
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

"""
def imprimirTview(pmatriz):
    contl = 0
    contp = 0
    tviewfra.delete(*tviewfra.get_children())
    for l in pmatriz:
        tviewfra.insert('', str(contl), 'C'+str(contl), text=l[3])
        for p in l[1]:
            tviewfra.insert('C'+str(contl), str(contp), 'F'+str(contp), text=p)
            contp += 1
        contl += 1
    return ''
"""


def auxllamarFBus(pnum):
    try:
        pnum = int(pnum)
        return True, pnum
    except ValueError:
        return False, pnum

"""
def llamarFBus():
    global pfrases
    print(pfrases)
    if verificarRed():
        num = pcan.get()
        tup = auxllamarFBus(num)
        if tup[0]:
            if tup[1] >= 0:
                matriz = crearMatriz(tup[1])
                dicc = crearDict(matriz)
                texto = sacarMayor(dicc, matriz)
                pdict.set(texto)
                imprimirTview(matriz)
            else:
                messagebox.showwarning('Numero Negativo', 'Porfavor solo digite numeros positivos (Mayor o Igual a 0)')
        else:
            messagebox.showerror('Numero Invalido', 'El valor digitado no es numerico, porfavor digite solo numeros')
    else:
        messagebox.showwarning('Sin Conexion', 'No hay conexion a Internet, revise e intente de nuevo')
    return ''
"""


# - FIN - #

