import json
from math import e
import random
from mainDir.neuralnetwrok import NeuronLayer
from mainDir.neuralnetwrok import Weights

learningRate = 0.5

layersFileName = "layers.json"


class NeuralNetwork:

    # region 1. Init Object

    def __init__(self, numberOfLayers=None, layersSize=None, biases=None, modelName="model/"):

        self.__modelName = modelName
        self.__loss = 0

        if numberOfLayers is None:
            if layersSize is None:
                self.readFromJson()
            else:
                self.__layersSize = layersSize
                self.__numberOfLayers = len(layersSize)

        else:
            self.__numberOfLayers = numberOfLayers
            self.__layersSize = layersSize

        if self.getNumberOfLayers() == 0:
            self.saveToJson(self.__layersSize)

        if biases is None:
            self.__biases = [0] * self.__numberOfLayers
        else:
            self.__biases = biases

        self.__weights = Weights.Weights(modelName=self.__modelName)

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
        if self.__weights.getNumberOfWeights() == 0:
            self.__weights.createJsonFile()
            self.addingWeights()
            self.__weights.saveAllWeights()
            self.__weights.buildIndexMatrix(self.getLayersSizeSim())

            print("The values is saved in database")
        else:
            self.__weights.buildIndexMatrix(self.getLayersSizeSim())


    # endregion

    # region 3. Adding weights between Neurons

    def addingWeightBetweenTwoNeuron(self, nId1, nId2, weight):
        id1 = min(nId1, nId2)
        id2 = max(nId1, nId2)
        self.__weights.insertToList(id1, id2, weight)

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
        self.__weights.loadWeightsToObject()
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
        self.__loss += totalError

    def calculatingLoss(self, numberOfErrors):
        self.__loss = self.__loss / numberOfErrors

    def clearLoss(self):
        self.loss = 0

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

        self.__weights.saveAllWeights()

    # endregion

    # region 9. Getters and Setters
    def getLayersSizeSim(self):
        sum = 0
        for layerSize in self.__layersSize:
            sum += layerSize

        return sum

    def getLayerByIndex(self, index):
        return self.__neuronLayers[index]

    def getWeightBetweenTwoNeuron(self, nId1, nId2):
        id1 = min(nId1, nId2)
        id2 = max(nId1, nId2)

        return float(self.__weights.getWeightByTwoNeuronId(id1, id2))

    def setWeightBetweenTwoNeuron(self, nId1, nId2, newWeight):
        id1 = min(nId1, nId2)
        id2 = max(nId1, nId2)
        self.__weights.setWeightByTwoNeuronId(id1, id2, newWeight)


    # endregion

    # region 10. Json file methods

    def getNumberOfLayers(self):
        try:
            layers = self.getLayersFromJson()
            return len(layers)
        except:
            return 0

    def getLayersFromJson(self):
        try:
            with open(self.__modelName + layersFileName, 'r') as jsonFile:
                layers = json.load(jsonFile)
        except :
            print("Cannot open the file")
            layers = []

        return layers

    def readFromJson(self):
        self.__numberOfLayers = None
        self.__layersSize = []

        layers = self.getLayersFromJson()
        self.__numberOfLayers = len(layers)
        self.__layersSize = [0] * self.__numberOfLayers

        for layer in layers:
            index = layer['index']
            layerSize = layer['size']
            self.__layersSize[index] = layerSize



    def saveToJson(self, layersSize):
        layers = []
        for i in range(len(layersSize)):
            newLayer = {
                'index': i,
                'size': layersSize[i]
            }
            layers.append(newLayer)

        with open(self.__modelName + layersFileName, 'w') as jsonFile:
            json.dump(layers, jsonFile, indent=4, sort_keys=True)

    # endregion

    # region 11. Prints

    def printLoss(self, numberOfErrors=1):
        self.calculatingLoss(numberOfErrors=numberOfErrors)
        print("Loss: " + str(self.__loss * 100) + "%")
        self.clearLoss()

    def printNameAndValue(self):
        neurons = self.getLayerByIndex(self.__numberOfLayers-1).getNeurons()
        for neuron in neurons:
            print(neuron.getName(), neuron.getValue() * 100, end='%\n')
        print()

    # endregion
