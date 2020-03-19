from mainDir.neuralnetwrok.NeuralNetwork import NeuralNetwork
from mainDir.picture.Picture import Picture
import xml.etree.ElementTree as ET
import cv2


class ObjectDetector:

    # region 1. Init object

    def __init__(self, model, labelmap):
        self.__model = model
        self.__labelmap = labelmap
        self.__neuralNetwork = NeuralNetwork(modelName="models/" + model + "/")

        self.__picture = Picture()
        self.__boxes = []
        self.__percentAndName = []
        self.__img = None

    # endregion

    # region 2. Setup the Neural Network

    def setupNeuralNetwork(self):
        items, modelName, imgHeight, imgWidth = self.readingInputFromXML(self.__labelmap)

        self.__neuralNetwork.creatNeuralNetwork()
        self.__neuralNetwork.creatingWeights()
        self.__neuralNetwork.addingOutputNeuronsName(items)

        self.__width = imgWidth
        self.__height = imgHeight

    # endregion

    # region 3. Picture methods

    def loadImage(self, img):
        self.__img = img
        self.__picture = Picture(img=self.__img, w=self.__width, h=self.__height)

    # endregion

    # region 4. Reading information from labelmap

    def readingInputFromXML(self, name):
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

    # endregion

    # region 5. Calculating

    def loadBoxes(self):
        self.__boxes = self.__picture.getBoxes()

    def detectingObjects(self):
        self.__percentAndName.clear()
        for box in self.__boxes:
            start, end = box
            self.__picture.cropImg(start[0], start[1], end[0], end[1])
            self.__picture.resizeNewImg(w=self.__width, h=self.__height)
            inputList = self.__picture.calculatingInput()
            self.__neuralNetwork.addingInput(inputValues=inputList)
            self.__neuralNetwork.calculatingValuesOfNeurons()
            self.__percentAndName.append(self.__neuralNetwork.getBestResult())

    # endregion
