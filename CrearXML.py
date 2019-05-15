import smtplib
import imaplib
import os
import xml.etree.ElementTree as et
from xml.dom import minidom

msrvr = imaplib.IMAP4_SSL("imap.gmail.com", 993)
base_path = os.path.dirname(os.path.realpath(__file__))
xml_file = os.path.join(base_path,"books.xml")
tree = et.parse(xml_file) # lo guarda en memoria
root = tree.getroot()


def crearFrase(id,frase,nom,cod):
    nuevoPersonaje = et.SubElement(root, "Personaje", attrib={"id": nom})
    nuevoID = et.SubElement(nuevoPersonaje,"id")
    nuevaFrase = et.SubElement(nuevoPersonaje, "Frase")
    nuevoCod = et.SubElement(nuevoPersonaje, "cod")

    nuevoPersonaje.text = nom
    nuevoCod.text = cod
    nuevoID.text = id
    nuevaFrase.text = frase

    tree.write(xml_file)



"""""
for child in root:
    print(child.text)
    for element in child:
        print(element.tag,":", element.text)
"""""