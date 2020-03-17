import time
from mainDir.neuralnetwrok import NeuralNetwork

def training(neuralNetwork):
    while True:
        neuralNetwork.addingInput([0.05, 0.1], "true")
        neuralNetwork.calculatingValuesOfNeurons()
        neuralNetwork.calculatingError()
        neuralNetwork.backPropagation()
        neuralNetwork.printLoss()
        neuralNetwork.printNameAndValue()

        time.sleep(0.1)

def main():

    layersSize = [2, 2, 2]
    neuralNetwork = NeuralNetwork.NeuralNetwork(layersSize=layersSize, modelName="models/test_model/")
    neuralNetwork.creatNeuralNetwork()
    neuralNetwork.creatingWeights()
    neuralNetwork.addingOutputNeuronsName(["false", "true"])
    training(neuralNetwork)


main()
