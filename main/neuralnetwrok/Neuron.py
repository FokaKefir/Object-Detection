class Neuron:

    # region 1. Init Object
    def __init__(self, id, value=0, name=""):
        self.__id = id
        self.__value = value
        self.__name = name
        self.__derErrorPerOut = 0

    # endregion

    # region 2. Getters and Setters

    def getId(self):
        return self.__id

    def getValue(self):
        return self.__value

    def getName(self):
        return self.__name

    def getDerErrorPerOut(self):
        return self.__derErrorPerOut

    def setId(self, newId):
        self.__id = newId

    def setValue(self, newValue):
        self.__value = newValue

    def setName(self, newName):
        self.__name = newName

    def setDerErrorPerOut(self, newDerErrorPerOut):
        self.__derErrorPerOut = newDerErrorPerOut

    # endregion