import json

modelDir = "model/"
weightsFileName = "weights.json"


class Weights:

    # region 1. Init

    def __init__(self):
        self.__weights = []
        self.__indexes = [[]]

    # endregion

    # region 2. Create json file

    def createJsonFile(self):
        with open(modelDir + weightsFileName, 'w') as jsonFile:
            json.dump([], jsonFile)

    # endregion

    # region 3. Insert to the json file

    def insertToList(self, nId1, nId2, weight=0):
        newWeight = {
            'nId1': nId1,
            'nId2': nId2,
            'weight': weight
        }
        self.__weights.append(newWeight)

    # endregion

    # region 4. Getters values from json file

    def loadWeightsToObject(self):
        self.__weights = self.getWeights()

    def getWeights(self):
        try:
            with open(modelDir + weightsFileName, 'r') as jsonFile:
                weights = json.load(jsonFile)
        except:
            weights = []
            print("Cannot open the file")
        return weights

    def getWeightByTwoNeuronId(self, nId1, nId2):

        index = self.getIndexFromIdes(nId1, nId2)

        return self.__weights[index]['weight']

    def getNumberOfWeights(self):
        weights = self.getWeights()
        return len(weights)

    # endregion

    # region 5. Update values at the json file

    def setWeightByTwoNeuronId(self, nId1, nId2, newWeight):
        self.__weights = self.getWeights()
        index = self.getIndexFromIdes(nId1, nId2)

        self.__weights[index]['weight'] = newWeight

    def saveAllWeights(self):
        self.setWeights(self.__weights)

    def setWeights(self, weights):
        with open(modelDir + weightsFileName, 'w') as jsonFile:
            json.dump(weights, jsonFile, indent=4, sort_keys=True)

    # endregion

    # region 6. Build index matrix

    def getIndexFromIdes(self, nId1, nId2):
        return self.__indexes[nId1][nId2]

    def buildIndexMatrix(self, number):
        self.__indexes = [[0] * number for _ in range(number)]
        index = 0
        weights = self.getWeights()
        for weight in weights:
            id1 = weight['nId1']
            id2 = weight['nId2']
            self.__indexes[id1][id2] = index
            self.__indexes[id2][id1] = index
            index += 1

    # endregion
