from neuralnetwrok import Neuron


class NeuronLayer:

    # region 1. Init Object
    def __init__(self, numberOfNeurons, bias, actuallyId):
        self.__numberOfNeurons = numberOfNeurons
        self.__actuallyId = actuallyId
        self.__bias = bias

    # endregion

    # region 2. Creat Layers

    def creatLayer(self):
        self.__neurons = []
        for i in range(self.__numberOfNeurons):
            newNeuron = Neuron.Neuron(self.__actuallyId)
            self.__neurons.append(newNeuron)
            self.__actuallyId += 1

    # endregion

    # region 3. Adding values for Neurons

    def addingValuesForNeurons(self, values):
        for i in range(self.__numberOfNeurons):
            val = values[i]
            self.__neurons[i].setValue(val)

    # endregion

    # region 4. Getters and Setters

    def getActuallyId(self):
        return self.__actuallyId

    def getNeurons(self):
        return self.__neurons

    def getBias(self):
        return self.__bias

    def setActuallyId(self, newId):
        self.__actuallyId = newId

    def setNeuronsDerErrorPerOut(self, newValue):
        for neuron in self.__neurons:
            neuron.setDerErrorPerOut(newValue)

    # endregion
