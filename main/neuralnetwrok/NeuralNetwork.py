from math import e
import random
from main.neuralnetwrok import NeuronLayer
from main.neuralnetwrok import Weights


learningRate = 0.5
databaseName = "NeuralNetwork_database"
class NeuralNetwork:

    # region 1. Init Object

    def __init__(self, numberOfLayers, layersSize, biases):
        self.__numberOfLayers = numberOfLayers
        self.__layersSize = layersSize
        self.__biases = biases

        self.__weights = Weights.Weights(databaseName)
        self.__weights.createDatabase()

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

        self.__weights.createTable()
        if self.__weights.getRowsSize() == 0:
            self.addingWeights()

    # endregion

    # region 3. Adding weights between Neurons

    def addingWeightBetweenTwoNeuron(self, nId1, nId2, weight):
        id1 = min(nId1, nId2)
        id2 = max(nId1, nId2)
        self.__weights.insertToTheTable(id1, id2, weight)

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

        return float(self.__weights.getWeightByTwoNeuronId(id1, id2))

    def setWeightBetweenTwoNeuron(self, nId1, nId2, newWeight):
        id1 = min(nId1, nId2)
        id2 = max(nId1, nId2)
        self.__weights.setWeightByTwoNeuronId(id1, id2, newWeight)


    # endregion

    # region 10. Prints

    def printWeights(self):
        for weight in self.__weights:
            print(weight)

    def printError(self):
        print(self.__totalError)

    def printNameAndValue(self):
        neurons = self.getLayerByIndex(self.__numberOfLayers-1).getNeurons()
        for neuron in neurons:
            print(neuron.getName(), neuron.getValue())
        print()
    # endregion
