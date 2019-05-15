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


import os
import xml.etree.ElementTree as et

import imaplib, email, os
import poplib
from tkinter import messagebox


import smtplib
import imaplib
import os
import xml.etree.ElementTree as et
import re
from xml.dom.minidom import parseString
from xml.dom import minidom

import smtplib
import imaplib
import os
import xml.etree.ElementTree as et
from xml.dom import minidom


msrvr = imaplib.IMAP4_SSL("imap.gmail.com", 993)
base_path = os.path.dirname(os.path.realpath(__file__))
xml_file = os.path.join(base_path,"books.xml")
tree = et.parse(xml_file) # lo guarda en memoria11
root = tree.getroot()
_xml_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)


base_path = os.path.dirname(os.path.realpath(__file__))
xml_file = os.path.join(base_path, "books.xml")
tree = et.parse(xml_file) # lo guarda en memoria
root = tree.getroot()

# Variable Global
pfrases = []

# Definición de Funciones

def crearFrase(id,frase,nom,cod):
    msrvr = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    base_path = os.path.dirname(os.path.realpath(__file__))
    xml_file = os.path.join(base_path, "books.xml")
    tree = et.parse(xml_file)  # lo guarda en memoria
    root = tree.getroot()

    nuevoPersonaje = et.SubElement(root, "Personaje", attrib={"id": nom})
    nuevoID = et.SubElement(nuevoPersonaje,"id")
    nuevaFrase = et.SubElement(nuevoPersonaje, "Frase")
    nuevoCod = et.SubElement(nuevoPersonaje, "cod")

    nuevoPersonaje.text = nom
    nuevoCod.text = cod
    nuevoID.text = id
    nuevaFrase.text = frase

    tree.write(xml_file)



def mejorarXML(xml, indent="  "):
    """""
            Entrada: el xml, una identeacion corta
            salida: el xml arreglado
            restriccion: si el xml ya esta arreglado no madna de una vez
        """""
    xml_re = _xml_re
    # avoid re-prettifying large amounts of xml that is fine
    if xml.count("\n") < 20:
        pxml = parseString(xml).toprettyxml(indent)
        return xml_re.sub('>\g<1></', pxml)
    else:
        return xml

def Enviar():
    """""
        Entrada: ninguna
        salida: el correo enviado
        restriccion: ninguna
    """""
    enviarCorreo("Back up2", mejorarXML(open("books.xml","r").read()))


def enviarCorreo(asunto,mensaje):
    origen = "proyectopythondanseb@gmail.com"
    password = "softskills01"
    destinario = origen
    mensaje = "Subject: {}\n\n{}".format(asunto,mensaje)
    print("origen: "+origen)
    print("contra: "+password)
    print("destinaripo:" + destinario)
    print("mensaje: "+mensaje)
    print("asunto:" + asunto)
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(origen,password)
    server.sendmail(origen,origen,mensaje)
    server.quit()
    return "Se ha enviado un back up a tu correo"




def backUp():
    m = poplib.POP3_SSL('pop.gmail.com', 995)  # se conecta al server
    m.user('proyectopythondanseb@gmail.com')  # inicia con correo
    m.pass_('softskills01')  # inicia con la password
    """""
    Entrada: ninguna
    salida: xmlNuevo2 con el mensaje del correo
    restriccion: debe haber un back up
    """""
    numero = len(m.list()[1]) # devuelve la cantidad de mensajes que hay en la bandeja
    if numero == 0:
        messagebox.showerror('No se ha encontrado un back up', 'Error: no hay un back up en el correo')
        return "<FrasesStarWars title='Progra2'>\n\n</FrasesStarWars>"
    for i in range(numero): # recorreo cada linea del mensaje del correo
        response, headerLines, bytes = m.retr(i+1) # le asigna a las variables el contenido del mensaje
    i = 12 # se usa el 12 porque en la informacion, las posicion 12 corresponde unicamente al mensaje
    xmlNuevo= "" # crea un string vacio
    while True: # ciclo semi infinito
        # print("\nPosicion:",i,headerLines[i])
        try:
            s = str(headerLines[i]) # instancia la s como el contenido tomado previamente en la parte del inicio del mensaje
            print("Cada i: ",headerLines[i]) # impresion de informacion para super usuario
            xmlNuevo = xmlNuevo + s.replace("b'","")+"\n" # limpia los bytes del correo
            i= i+1 # se mueve a la siguiente linea del correo
        except: # cuando no hay mas lineas se sale del index
            break # cuando no hay mas lineas se sale del ciclo
    xmlNuevo2 = "" # crea un nuevo string
    s = str(xmlNuevo) # instancia la s como el string del xml creado
    xmlNuevo2 = s.replace("'","") # a xml2 le quita los bytes sobrantes
    # print(xmlNuevo2)
    # print("ce fini")
    return xmlNuevo2 # retorna el xml convertido de byte a string

def verificarRed():
    """
    Funcion: Verifica si el usuario tiene acceso a Internet
    Entradas: N/A
    Salidas: Booleano True/False - si cumple los requisitos
    """
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
    """
    Funcion: Crea una lista con todas las respuestas de la API las veces que el usuario solicita
    Entradas: `pcan`(int) valor a analizar
    Salidas: `pfrases`(list) resultado del proceso
    """
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
    """
    Funcion: Saca el nombre de la key 'starWarsQuote' del dict `pfrases` y crea una nueva key con el nombre
    Entradas: N/A
    Salidas: `pfrases`(list) resultado del proceso
    """
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
    """
    Funcion: Corrige el error si crea mas de 2 elementos al hacer split
    Entradas: `ptexto`(list) valor analizar
    Salidas: `ptexto`(list) resultado del proceso
    """
    f = len(ptexto) - 1
    for l in range(1, f):
        ptexto[0] = ptexto[0] + ' - ' + ptexto[l]
    while f > 1:
        ptexto.pop(1)
        f -= 1
    return ptexto


def eliminarFRep():
    """
    Funcion: Elimina los diccionarios repetidos dentro de una lista
    Entradas: N/A
    Salidas: `pfrases`(list) resultado del proceso
    """
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
    """
    Funcion: Crea el codigo de aplicacion de cada diccionario y se lo añade con la key 'cod'
    Entradas: N/A
    Salidas: `pfrases`(list) resultado del proceso
    """
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
    """
    Funcion: Reproduce una lista de funciones y se las asigna a lista (diccionario con todas las keys)
    Entradas: `pcan`(str) valor a analizar
    Salidas: `lista`(list) resultado del proceso
    """
    lista = []
    global pfrases
    pfrases = sacarFrases(pcan)
    pfrases = eliminarFRep()
    pfrases = sacarNombre()
    pfrases = crearCdA()
    for p in pfrases:
        lista.append(p)
    return lista


def crearMatriz(pcan):
    """
    Funcion: Crea una matriz a partir de `pfrases`(list) que sera utilizada para imprimir la informacion
    Entradas: `pcan`(str) valor a analizar
    Salidas: `matriz`(list) resultado del proceso
    """
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
    """
    Funcion: Crea un diccionario con el codigo de la aplicacion de key y la cantidad de respuesta de la API con ese pj
    Entradas: `pmatriz`(list) valor a analizar
    Salidas: `diccfrases`(dict) resultado del proceso
    """
    diccfrases = {}
    for per in pmatriz:
        cod = per[3]
        diccfrases[cod] = len(per[2])
    return diccfrases


def sacarMayor(pdict, pmatriz):
    """
    Funcion: Revisa el dictionario y la matriz creadas para verificar cual es el pj mas citado en la aplicacion
    Entradas: `pdict`(dict) y `pmatriz`(list) valores a analizar
    Salidas: str('Mas Citado + `nombre del pj mas citado en el dict`)
    """
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
    """
    Funcion: Verifica si el dato ingresado es un numero entero
    Entradas: `pnum`(str) valor a analizar
    Salidas: {tuple} (Bool, `pnum`(int)) resultado del proceso
    """
    try:
        pnum = int(pnum)
        return True, pnum
    except ValueError:
        return False, pnum


# - FIN - #
