import imaplib, email, os
import poplib


m = poplib.POP3_SSL('pop.gmail.com',995)
m.user('proyectopythondanseb@gmail.com')
m.pass_('softskills01')

def backUp():
    numero = len(m.list()[1])
    for i in range(numero):
        response, headerLines, bytes = m.retr(i+1)
    i = 12
    xmlNuevo= ""
    while True:
        #print("\nPosicion:",i,headerLines[i])
        try:
            s = str(headerLines[i])
            print("Cada i: ",headerLines[i])
            xmlNuevo = xmlNuevo + s.replace("b'","")+"\n"
            i= i+1
        except:
            break
    xmlNuevo2 = ""
    s = str(xmlNuevo)
    xmlNuevo2 = s.replace("'","")
    #print(xmlNuevo2)
    #print("ce fini")
    return xmlNuevo2

