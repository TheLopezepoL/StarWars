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
from tkinter import *
from tkinter import Text
from tkinter import Tk
from tkinter import ttk
from tkinter import messagebox
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


def sacarNombre(pfrases):
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


def eliminarFRep(pfrases):
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


def crearMatriz(pcan):
    matriz = []
    nom = ''
    cont = 0
    frases = sacarFrases(pcan)
    frases = eliminarFRep(frases)
    frases = sacarNombre(frases)
    frases = crearCdA(frases)
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



def auxllamarFBus(pnum):
    try:
        pnum = int(pnum)
        return True, pnum
    except ValueError:
        return False, pnum


def llamarFBus():
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


# Programa Principal
# # # raiz
raiz = Tk()
style = ttk.Style()
style.theme_use('clam')
raiz.title("Frases de Star Wars")
raiz.config(bg="black")
raiz.resizable(0, 0)
raiz.iconbitmap('logo.ico')
raiz.geometry("800x450")
pcan = StringVar()
prfrases = StringVar()
pdict = StringVar()
# fondo
imagen = PhotoImage(file='fondo.png')
fondo = Label(raiz, image=imagen).place(x=-11, y=-8)
#
# # # texto buscar
texbus = Entry(fondo, bg='yellow', textvariable=pcan)
texbus.place(x=500, y=100)
texbus.config(width='5', font=('Fixedsys', 23), bd=10, relief='ridge')
# # # boton buscar
botbus = Button(fondo, text='Buscar', bg='yellow', fg='Black', font="Fixedsys", command=lambda: llamarFBus())
botbus.place(x=610, y=98)
botbus.config(width="15", height="2", bd=10, relief='ridge', cursor='hand2')
# # # boton enviar xml
botenv = Button(fondo, text='Enviar XML', bg='yellow', fg='Black', font='Fixedsys')
botenv.place(x=497, y=188)
botenv.config(width='29', height='2', bd=10, relief='ridge', cursor="hand2")
###
texdic = Entry(fondo, bg='black', fg="Yellow", bd=1, relief='flat', textvariable=pdict)
texdic.place(x=497, y=276)
texdic.config(width='31', font=('Fixedsys', 10))
# # # frame frases
ffra = Frame(fondo, width=415, height=335, bg='black')
ffra.place(x=50, y=40)
# # # frame list box
flbfra = Frame(ffra, width=400, height=335, bg='black')
flbfra.grid(row=0, column=0)
# # #
style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Fixedsys', 12), fg='Yellow')
style.configure("mystyle.Treeview.Heading", font=('Fixedsys', 12,'bold'), fg='Yellow')
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
# # # texto frases
tviewfra = ttk.Treeview(flbfra, style="mystyle.Treeview", selectmode='extended', columns='A')
tviewfra.grid(row=0, column=0)
tviewfra.pack(expand=True, fill='both')
tviewfra.column("#0", minwidth=100, width=200, stretch=True)
tviewfra.config(height=17)
#
print(style.element_options("Vertical.TScrollbar.thumb"))
# configure the style
style.configure("Vertical.TScrollbar", gripcount=0,
                background="yellow", darkcolor="gold3", lightcolor="yellow2",
                troughcolor="black", bordercolor="black", arrowcolor="black")
#
sbarfra = ttk.Scrollbar(ffra, command=tviewfra.yview, orient="vertical")
sbarfra.grid(row=0, column=1, sticky='nsew')
tviewfra.config(yscrollcommand=sbarfra.set)
#
# # # boton manual de usuario
mdu = Button(fondo, text="-> Manual de Usuario <-", bg='black', fg='White', font='Fixedsys')
mdu.pack(side="bottom", fill='x')
mdu.config(cursor='hand2', bd=1, relief='flat')
###
raiz.mainloop()
###
# - FIN - #

