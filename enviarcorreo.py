import smtplib
import imaplib
import os
import xml.etree.ElementTree as et
from xml.dom import minidom


#variables globales
msrvr = imaplib.IMAP4_SSL("imap.gmail.com", 993)
base_path = os.path.dirname(os.path.realpath(__file__))
xml_file = os.path.join(base_path,"books.xml")
tree = et.parse(xml_file) # lo guarda en memoria
root = tree.getroot()

listaPersonajes = []


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

def xml():
    mydoc = minidom.parse('books.xml')
    personaje = mydoc.getElementsByTagName('personaje')
    frase = mydoc.getElementsByTagName('frase')
    todos = mydoc.getElementsByTagName('TodosPersonajes')

    #imprimir todos por el contenido del tag
    print('imprimir todos por el contenido del tag') 
    for personajes in personaje:
        print(personajes.firstChild.data)

    print('imprimir todos por el contenido del tag en frases') 
    for frases in frase:
        print(frases.firstChild.data)

    # imprimir todos por el nombre del tag
    print('\nimprimir todos por el name= del tag')  
    for personajes in personaje:  
        print(personajes.attributes['name'].value)

    print('\nImprimir la key de la frase')  
    for frases in frase:  
        print(frases.attributes['frase'].value)
        

    archivoXML = "books.xml"
    print(archivoXML)

    #dom = ElementTree.parse(archivoXML)
    #personaje = dom.findall("TodosPersonajes")
    print("_______")
    for i in personaje:
        print("AAAAimprimir contenido de tag ", i.text)
    print("#####")
    for j in personaje:
        vpersonje = j.find("personaje")
        vfrase = j.find("frase")
        print(" este mae: {} dijo: {}".format(vpersonje.text,vfrase.text))
    print("&8888")

def crearFrase(id,frase,personaje):
    nuevoPersonaje = et.SubElement(root, "Personaje", attrib={"id": id})
    nuevaFrase = et.SubElement(nuevoPersonaje, "Frase")
    nuevoPersonaje.text = personaje
    nuevaFrase.text = frase
    tree.write(xml_file)

#crearFrase("Luke", "hosd ajaj", "Luke")
#crearFrase("Luke", "hola si ajaj", "Luke")
#crearFrase("Yoda", "asdasd", "Yoda")

#imprime todas las frases


mydoc = minidom.parse('books.xml')
personaje = mydoc.getElementsByTagName('Personaje')
frase = mydoc.getElementsByTagName('Frase')


for child in root:
    print(child.text)
    for element in child:
        print(element.tag,":", element.text)

for vpersonajes in root:
    if not vpersonajes.text in listaPersonajes:
        listaPersonajes.append(vpersonajes.text)

print("Todos los personajes: ")
for i in listaPersonajes:
    print(i)

f = open('books.xml', 'r')
file_contents = f.read()
enviarCorreo("back up", file_contents)
f.close()



