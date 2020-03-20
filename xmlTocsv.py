import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def readingInformationsFromXML(xmlFileName):
    xmlList = []
    tree = ET.parse(xmlFileName)
    root = tree.getroot()
    for member in root.findall("object"):
        value = (
            root.find("filename").text,
            int(root.find("size")[0].text),
            int(root.find("size")[0].text),
            member[0].text,
            int(member[4][0].text),
            int(member[4][1].text),
            int(member[4][2].text),
            int(member[4][3].text)
        )
        xmlList.append(value)
    return xmlList

def xmlTocsv(path):
    xmlList = []

    for xmlFile in glob.glob(path + "/*.xml"):
        new = readingInformationsFromXML(xmlFileName=xmlFile)
        xmlList.extend(new)

    xmlDF = pd.DataFrame(xmlList, columns=['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
    return xmlDF
    
def main():
    xmlDF = xmlTocsv("images/train")
    xmlDF.to_csv(("images/" + "train_labels.csv"), index=0)

main()