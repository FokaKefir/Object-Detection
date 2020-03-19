import random
import time
from mainDir.neuralnetwrok import NeuralNetwork
import csv
import xml.etree.ElementTree as ET
import cv2
from mainDir.picture import Picture


def readingInputFromXML(name):
    items = []

    tree = ET.parse(name)
    root = tree.getroot()

    modelName = str(root.findtext("modelName"))

    imageInfo = root.find("image")
    width = int(imageInfo[0].text)
    height = int(imageInfo[1].text)

    for member in root.findall("item"):
        items.append(str(member[0].text))

    return (items, modelName, height, width)


def getInformationsFromCSV():
    info = []

    with open("images/train_labels.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            info.append(row)

    info.pop(0)
    random.shuffle(info)
    return info


def calculatingInput(info, imgWidth, imgHeight):
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


def training():
    items, modelName, imgHeight, imgWidth = readingInputFromXML("labelmap.xml")
    inputLayer = imgHeight * imgWidth
    layersSize = [inputLayer, 10, 10, 10, len(items)]

    neuralNetwork = NeuralNetwork.NeuralNetwork(layersSize=layersSize, modelName="models/" + modelName + "/")
    neuralNetwork.creatNeuralNetwork()
    neuralNetwork.creatingWeights()
    neuralNetwork.addingOutputNeuronsName(items)

    infos = getInformationsFromCSV()


    while True:
        for info in infos:
            start = time.time()

            inputToTrain = calculatingInput(info, imgWidth, imgHeight)
            neuralNetwork.addingInput(inputValues=inputToTrain[0], result=inputToTrain[1])
            neuralNetwork.calculatingValuesOfNeurons()
            neuralNetwork.calculatingError()
            neuralNetwork.setLearningRate(neuralNetwork.getTotalError())
            neuralNetwork.backPropagation()

            end = time.time()
            print(round(end-start, 3), inputToTrain[1])
            neuralNetwork.printError()

        neuralNetwork.printLoss(len(infos))


if __name__ == '__main__':
    training()

