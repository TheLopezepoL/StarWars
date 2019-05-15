import imaplib, email, os
import poplib
from tkinter import messagebox

#variables globales
m = poplib.POP3_SSL('pop.gmail.com',995) # se conecta al server
m.user('proyectopythondanseb@gmail.com') # inicia con correo
m.pass_('softskills01') #inicia con la password

def backUp():
    """""
    Entrada: ninguna
    salida: xmlNuevo2 con el mensaje del correo
    restriccion: debe haber un back up
    """""
    numero = len(m.list()[1]) # devuelve la cantidad de mensajes que hay en la bandeja
    if numero == 0:
        return messagebox.showerror('No se ha encontrado un back up', 'Error: no hay un back up en el correo')
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

