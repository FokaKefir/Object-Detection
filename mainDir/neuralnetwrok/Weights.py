import json

modelDir = "model/"
weightsFileName = "weights.json"


class Weights:

    # region 1. Init

    def __init__(self):
        pass

    # endregion

    # region 2. Create json file

    def createJsonFile(self):
        with open(modelDir + weightsFileName, 'w') as jsonFile:
            json.dump([], jsonFile)

    # endregion

    # region 3. Insert to the json file

    def insertToJsonFile(self, nId1, nId2, weight=0):
        newWeight = {
            'nId1': nId1,
            'nId2': nId2,
            'weight': weight
        }
        weights = self.getWeights()
        weights.append(newWeight)
        self.setWeights(weights=weights)

    # endregion

    # region 4. Getters values from json file

    def getWeights(self):
        try:
            with open(modelDir + weightsFileName, 'r') as jsonFile:
                weights = json.load(jsonFile)
        except:
            weights = []
            print("Cannot open the file")
        return weights

    def getWeightByTwoNeuronId(self, nId1, nId2):
        weights = self.getWeights()
        first = 0
        last = len(weights) - 1
        index = 0
        while True:
            mid = int((first + last) / 2)
            if weights[mid]['nId2'] == nId2:
                index = mid
                break
            elif weights[mid]['nId2'] > nId2:
                last = mid - 1
            else:
                first = mid + 1

        if weights[index]['nId1'] != nId1:
            while weights[index]['nId1'] > nId1:
                index -= 1

            while weights[index]['nId1'] < nId1:
                index += 1

        return weights[index]['weight']


    def getNumberOfWeights(self):
        weights = self.getWeights()
        return len(weights)

    # endregion

    # region 5. Update values at the json file

    def setWeightByTwoNeuronId(self, nId1, nId2, newWeight):
        weights = self.getWeights()
        first = 0
        last = len(weights) - 1
        index = 0
        while True:
            mid = int((first + last) / 2)
            if weights[mid]['nId2'] == nId2:
                index = mid
                break
            elif weights[mid]['nId2'] > nId2:
                last = mid - 1
            else:
                first = mid + 1

        if weights[index]['nId1'] != nId1:
            while weights[index]['nId1'] > nId1:
                index -= 1

            while weights[index]['nId1'] < nId1:
                index += 1

        weights[index]['weight'] = newWeight
        self.setWeights(weights=weights)

    def setWeights(self, weights):
        with open(modelDir + weightsFileName, 'w') as jsonFile:
            json.dump(weights, jsonFile, indent=4, sort_keys=True)

    # endregion
