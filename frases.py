########################################
# Integrantes: Sebastián López Herrera y Daniel Sequeira Retana
# Fecha creación: 26/04/2019 12:00
# Ultima actualización: 14/05/2019 23:00
# Version 0.1 - Python 3.7.3
########################################
# Importación de Librerias
from tkinter import *
from tkinter import Tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser as wb
from funciones import *


import os

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


def llamarFBus():
    global pfrases
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


def abrirPDF():
    wb.open_new(r'C:\Users\thelo\Desktop\Frases\Manual tkinter 8.5 (2013-06-24).pdf')

def cerrar():
    num = pcan.get()
    tup = auxllamarFBus(num)
    if tup[0]:
        if messagebox.askyesno("Hacer Back Up", "¿Desea hacer un Back Up de las frases antes de salir?"):
            Enviar()
            messagebox.showinfo("May the force be with you", "Se ha enviado un Back up a tu correo")
            raiz.destroy()
        else:
            raiz.destroy()
    else:
        messagebox.showerror('No se hará Back Up', 'No hay frases para hacer un back up')
        raiz.destroy()


def cargarBackUp():
    if messagebox.askyesno("Cargar Back Up", "¿Desea cargar el ultimo Back Up de las frases?"):
        os.remove("books.xml")
        f = open ("books.xml","a")
        f.write(backUp())
        f.close()
    else:
        os.remove("books.xml")
        f = open("books.xml", "a")
        f.write("<FrasesStarWars title='Progra2'>\n\n</FrasesStarWars>")
        f.close()

def validarShare():
    num = pcan.get()
    tup = auxllamarFBus(num)
    if tup[0]:
        Enviar()
    else:
        messagebox.showerror('No se hará Back Up', 'No hay frases para hacer un back up')





# Programa Principal
# # # raiz
raiz = Tk()
cargarBackUp()
raiz.protocol("WM_DELETE_WINDOW", cerrar)
#raiz.wm_attributes('-fullscreen','true')
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
botbus = Button(fondo, text='Buscar', bg='yellow', fg='Black', font="Fixedsys", command=llamarFBus)
botbus.place(x=610, y=98)
botbus.config(width="15", height="2", bd=10, relief='ridge', cursor='hand2')
# # # boton enviar xml
botenv = Button(fondo, text='Share', bg='yellow', fg='Black', font='Fixedsys', command=validarShare)
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
tviewfra.column("#0", minwidth=0, width=400, stretch=False)
tviewfra.column('A', minwidth=0, width=0, stretch=False)
tviewfra.config(height=16)
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
mdu = Button(fondo, text="-> Manual de Usuario <-", bg='black', fg='White', font='Fixedsys', command=abrirPDF)
mdu.pack(side="bottom", fill='x')
mdu.config(cursor='hand2', bd=1, relief='flat')
###
raiz.mainloop()
###
# - FIN - #

