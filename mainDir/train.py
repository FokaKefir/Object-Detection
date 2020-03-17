from mainDir.neuralnetwrok import NeuralNetwork
import csv
import xml.etree.ElementTree as ET
import cv2
from mainDir.picture import Picture
imgWidth = 25
imgHeight = 25

def readingInputFromXML(name):
    items = []

    tree = ET.parse(name)
    root = tree.getroot()

    for member in root.findall("item"):
        items.append(str(member[0].text))

    return items

def getInformationsFromCSV():
    info = []

    with open("images/train_labels.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            info.append(row)

    info.pop(0)

    return info

def calculatingInput(info):
    dir = "images/train/"
    imgName = str(info[0])
    w = int(info[1])
    h = int(info[2])
    objectName = str(info[3])

    img = cv2.imread(dir + imgName, 0)

    pic = Picture.Picture(img, w, h)
    pic.cropImg(int(info[4]), int(info[5]), int(info[6]), int(info[7]))
    pic.resizeImg(imgWidth, imgHeight)
    iList = pic.calculatingInput()

    return (iList, objectName)

def training(items):
    inputLayer = imgHeight * imgWidth
    layersSize = [inputLayer, 3, 8, 8, 8, len(items)]
    infos = getInformationsFromCSV()

    neuralNetwork = NeuralNetwork.NeuralNetwork(layersSize=layersSize)
    neuralNetwork.creatNeuralNetwork()
    neuralNetwork.creatingWeights()
    neuralNetwork.addingOutputNeuronsName(items)

    while True:
        for info in infos:

            inputToTrain = calculatingInput(info)
            neuralNetwork.addingInput(inputValues=inputToTrain[0], result=inputToTrain[1])
            neuralNetwork.calculatingValuesOfNeurons()
            neuralNetwork.calculatingError()
            neuralNetwork.backPropagation()

        neuralNetwork.printError()
        neuralNetwork.printNameAndValue()

if __name__ == '__main__':
    items = readingInputFromXML("labelmap.xml")
    training(items)

