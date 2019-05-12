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
import tkinter


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
        nom = p['nom'].upper()
        li = nom[0]
        lf = nom[len(nom)-1]
        cod = li + str(ncod).zfill(3) + '-' + lf
        p['cod'] = cod
        ncod -= 1
    pfrases.reverse()
    return pfrases


# Programa Principal
#
from tkinter import *
from tkinter import Text
from tkinter import Tk
from tkinter import ttk
# # # raiz
raiz = Tk()
style = ttk.Style()
style.theme_use('clam')
raiz.title("Frases de Star Wars")
raiz.config(bg="black")
raiz.resizable(0, 0)
raiz.iconbitmap('logo.ico')
raiz.geometry("800x450")
# fondo
imagen = PhotoImage(file='fondo.png')
fondo = Label(raiz, image=imagen).place(x=-11, y=-8)
#
# # # texto buscar
tbus = Entry(fondo, bg='yellow') #LightGoldenrod1
tbus.place(x=500, y=100)
tbus.config(width='5', font=('Fixedsys', 23), bd=10, relief='ridge')
# # # boton buscar
fbus = Button(fondo, text='Buscar', bg='yellow', fg='Black', font="Fixedsys")
fbus.place(x=610, y=98)
fbus.config(width="15", height="2", bd=10, relief='ridge', cursor='hand2')
# # # boton enviar xml
fenv = Button(fondo, text='Enviar XML', bg='yellow', fg='Black', font='Fixedsys')
fenv.place(x=497, y=188)
fenv.config(width='29', height='2', bd=10, relief='ridge', cursor="hand2")
###
tdic = Entry(fondo, bg='black', fg="Yellow", bd=1, relief='flat')
tdic.place(x=497, y=276)
tdic.config(width='31', font=('Fixedsys', 10))
# # # frame frases
ffra = Frame(fondo, width=415, height=335, bg='black')
ffra.place(x=50, y=50)
# # # texto frases
tfra = Text(ffra, width=50, height=23, bg='Black', fg='yellow', font='Fixedsys')
tfra.grid(row=0, column=0,)
tfra.config(bd=1, relief='flat')
#
print(style.element_options("Vertical.TScrollbar.thumb"))

# configure the style
style.configure("Vertical.TScrollbar", gripcount=0,
                background="yellow", darkcolor="gold3", lightcolor="yellow2",
                troughcolor="black", bordercolor="black", arrowcolor="black")
#
sfra = ttk.Scrollbar(ffra, command=tfra.yview, orient="vertical")
sfra.grid(row=0, column=1, sticky='nsew')
tfra.config(yscrollcommand=sfra.set)
#
# # # boton manual de usuario
mdu = Button(fondo, text="-> Manual de Usuario <-", bg='black', fg='White', font='Fixedsys')
mdu.pack(side="bottom", fill='x')
mdu.config(cursor='hand2', bd=1, relief='flat')
###
raiz.mainloop()
###


if verificarRed():
    frases = sacarFrases(5)  #El tiempo de respuesta puede fallar
    frases = eliminarFRep(frases)
    frases = sacarNombre(frases)
    frases = crearCdA(frases)
    print(len(frases))
    print(frases)
else:
    print('Nel we')



# - FIN - #