from math import e
import random
from mainDir.neuralnetwrok import NeuronLayer
from mainDir.neuralnetwrok import Weights
import sqlite3
from sqlite3 import Error

learningRate = 0.25
databaseName = "NNdb.db"
directory = "databases/"
class NeuralNetwork:

    # region 1. Init Object

    def __init__(self, numberOfLayers=None, layersSize=None, biases=None):
        self.__conn = sqlite3.connect(directory + databaseName)
        self.createTheTable()

        if numberOfLayers is None:
            if layersSize is None:
                self.readFromTable()
            else:
                self.__layersSize = layersSize
                self.__numberOfLayers = len(layersSize)

        else:
            self.__numberOfLayers = numberOfLayers
            self.__layersSize = layersSize


        if self.getTableSize() == 0:
            self.saveToTable(self.__layersSize)

        if biases is None:
            self.__biases = [0] * self.__numberOfLayers
        else:
            self.__biases = biases

        self.__weights = Weights.Weights(databaseName)

    # endregion

    # region 2. Creat the Neural Network and Weight list

    def creatNeuralNetwork(self):
        id = 0
        self.__neuronLayers = []
        for index in range(self.__numberOfLayers):
            layerSize = self.__layersSize[index]
            bias = self.__biases[index]
            newNeuronLayer = NeuronLayer.NeuronLayer(layerSize, bias, id)
            newNeuronLayer.creatLayer()
            self.__neuronLayers.append(newNeuronLayer)

            id = newNeuronLayer.getActuallyId()

    def creatingWeights(self):

        self.__weights.createTable(self.__conn)
        if self.__weights.getRowsSize(self.__conn) == 0:
            self.addingWeights()
            print("The values is saved in database")

    # endregion

    # region 3. Adding weights between Neurons

    def addingWeightBetweenTwoNeuron(self, nId1, nId2, weight):
        id1 = min(nId1, nId2)
        id2 = max(nId1, nId2)
        self.__weights.insertToTheTable(self.__conn, id1, id2, weight)

    def addingWeightsBetweenTwoLayer(self, layer1, layer2):
        neurons1 = layer1.getNeurons()
        neurons2 = layer2.getNeurons()
        for neuronFromLayer2 in neurons2:
            for neuronFromLayer1 in neurons1:
                neuronId1 = neuronFromLayer1.getId()
                neuronId2 = neuronFromLayer2.getId()
                weight = random.uniform(0, 1)
                self.addingWeightBetweenTwoNeuron(neuronId1, neuronId2, weight)

    def addingWeights(self):
        for i in range(self.__numberOfLayers - 1):
            layer1 = self.getLayerByIndex(i)
            layer2 = self.getLayerByIndex(i + 1)
            self.addingWeightsBetweenTwoLayer(layer1, layer2)

    # endregion

    # region 4. Adding output neurons name

    def addingOutputNeuronsName(self, names):
        layer = self.getLayerByIndex(self.__numberOfLayers - 1)
        neurons = layer.getNeurons()
        for i in range(len(neurons)):
            neurons[i].setName(names[i])

    # endregion

    # region 5. Adding input

    def addingInput(self, inputValues, result):
        self.getLayerByIndex(0).addingValuesForNeurons(inputValues)
        self.__result = result

    # endregion

    # region 6. Forward
    def calculatingNeuronsValueBetweenTwoLayer(self, layerIn, layerOut):
        neuronsIn = layerIn.getNeurons()
        neuronsOut = layerOut.getNeurons()
        bias = layerOut.getBias()
        for neuronOut in neuronsOut:
            net = 0
            neuronOutId = neuronOut.getId()
            for neuronIn in neuronsIn:
                neuronInId = neuronIn.getId()
                neuronInValue = neuronIn.getValue()
                weight = self.getWeightBetweenTwoNeuron(neuronInId, neuronOutId)
                net += neuronInValue * weight

            net += bias
            out = 1 / (1 + e ** (-1 * net))
            neuronOut.setValue(out)

    def calculatingValuesOfNeurons(self):
        for i in range(self.__numberOfLayers - 1):
            layerIn = self.getLayerByIndex(i)
            layerOut = self.getLayerByIndex(i + 1)
            self.calculatingNeuronsValueBetweenTwoLayer(layerIn, layerOut)

    # endregion

    # region 7. Calculating error
    def calculatingError(self):
        neurons = self.getLayerByIndex(self.__numberOfLayers-1).getNeurons()
        totalError = 0
        for neuron in neurons:
            name = neuron.getName()
            if(name == self.__result):
                target = 0.99
            else:
                target = 0.01
            error = ((target - neuron.getValue()) ** 2)/2
            totalError += error
        self.__totalError = totalError


    # endregion

    # region 8. Backward

    def calculatingDerErrorPerOut(self, neuronIn, neuronOut, condition):
        nOutValue = neuronOut.getValue()

        if (condition):
            if (neuronOut.getName() == self.__result):
                target = 0.99
            else:
                target = 0.01
            derErrorPerOut = nOutValue - target

        else:
            derErrorPerOut = neuronIn.getDerErrorPerOut()

        return derErrorPerOut

    def backPropagationBeetwenTwoLayer(self, layerOut, layerIn, condition):
        layerIn.setNeuronsDerErrorPerOut(0)

        neuronsOut = layerOut.getNeurons()
        neuronsIn = layerIn.getNeurons()

        for neuronOut in neuronsOut:
            for neuronIn in neuronsIn:
                nOutId = neuronOut.getId()
                nInId = neuronIn.getId()

                nOutValue = neuronOut.getValue()
                nInValue = neuronIn.getValue()

                derErrorPerOut = self.calculatingDerErrorPerOut(neuronIn, neuronOut, condition)
                derOutPerNet = nOutValue * (1 - nOutValue)
                derNetPerWeight = nInValue

                derErrorPerWeight = derErrorPerOut * derOutPerNet * derNetPerWeight

                newWeight = self.getWeightBetweenTwoNeuron(nInId, nOutId) - learningRate * derErrorPerWeight

                neuronIn.setDerErrorPerOut(
                    neuronIn.getDerErrorPerOut() + derErrorPerOut * derOutPerNet * self.getWeightBetweenTwoNeuron(nInId, nOutId))

                self.setWeightBetweenTwoNeuron(nInId, nOutId, newWeight)

    def backPropagation(self):
        for i in range(self.__numberOfLayers-1, 0, -1):
            layerOut = self.__neuronLayers[i]
            layerIn = self.__neuronLayers[i-1]
            condition = False
            if i == self.__numberOfLayers-1 :
                condition = True
            self.backPropagationBeetwenTwoLayer(layerOut, layerIn, condition)

    # endregion

    # region 9. Getters and Setters
    def getLayerByIndex(self, index):
        return self.__neuronLayers[index]

    def getWeightBetweenTwoNeuron(self, nId1, nId2):
        id1 = min(nId1, nId2)
        id2 = max(nId1, nId2)

        return float(self.__weights.getWeightByTwoNeuronId(self.__conn, id1, id2))

    def setWeightBetweenTwoNeuron(self, nId1, nId2, newWeight):
        id1 = min(nId1, nId2)
        id2 = max(nId1, nId2)
        self.__weights.setWeightByTwoNeuronId(self.__conn, id1, id2, newWeight)


    # endregion

    # region 10. Close the connection to database

    def getTableSize(self):
        cursor = self.__conn.cursor()
        try:
            cursor.execute("SELECT * FROM layers")
            return len(cursor.fetchall())

        except Error as error:
            return 0

    def saveToTable(self, layersSize):
        cursor = self.__conn.cursor()
        index = 0
        for layerSize in layersSize:
            newRow = (index, layerSize)
            cursor.execute("INSERT INTO layers VALUES (?, ?)", newRow)
            self.__conn.commit()
            index += 1

    def readFromTable(self):
        if self.getTableSize() == 0:
            print("Error: the table is empty")
            return

        cursor = self.__conn.cursor()

        cursor.execute("SELECT * FROM layers")

        layers = cursor.fetchall()
        self.__numberOfLayers = len(layers)

        self.__layersSize = [0] * self.__numberOfLayers
        for layer in layers:
            id = layer[0]
            layerSize = layer[1]
            self.__layersSize[id] = layerSize



    def createTheTable(self):
        cursor = self.__conn.cursor()
        try:
            cursor.execute('''CREATE TABLE layers (id int, size int)''')
        except Error as error:
            print(error)

    def closeConnection(self):
        self.__conn.close()

    # endregion

    # region 10. Prints

    def printError(self):
        print(self.__totalError)

    def printNameAndValue(self):
        neurons = self.getLayerByIndex(self.__numberOfLayers-1).getNeurons()
        for neuron in neurons:
            print(neuron.getName(), neuron.getValue())
        print()
    # endregion
