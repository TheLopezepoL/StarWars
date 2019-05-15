import os
import xml.etree.ElementTree as et


base_path = os.path.dirname(os.path.realpath(__file__))
xml_file = os.path.join(base_path, "data\\books.xml")
tree = et.parse(xml_file) # lo guarda en memoria
root = tree.getroot()
for child in root:
    print("hola", child.tag, child.attrib)
