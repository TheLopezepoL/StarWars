import smtplib
import imaplib
import os
import xml.etree.ElementTree as et
import re
from xml.dom.minidom import parseString
from xml.dom import minidom


#variables globales
msrvr = imaplib.IMAP4_SSL("imap.gmail.com", 993)
base_path = os.path.dirname(os.path.realpath(__file__))
xml_file = os.path.join(base_path,"books.xml")
tree = et.parse(xml_file) # lo guarda en memoria
root = tree.getroot()
_xml_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)

def mejorarXML(xml, indent="  "):

    xml_re = _xml_re
    # avoid re-prettifying large amounts of xml that is fine
    if xml.count("\n") < 20:
        pxml = parseString(xml).toprettyxml(indent)
        return xml_re.sub('>\g<1></', pxml)
    else:
        return xml

def Enviar():
    #f = open('books.xml', 'r')
    #file_contents = f.read()
    enviarCorreo("Back up2", mejorarXML(open("books.xml","r").read()))
    #f.close()

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

