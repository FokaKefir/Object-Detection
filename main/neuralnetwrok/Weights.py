import mysql.connector as mysql

class Weights:

    # region 1. Init

    def __init__(self, databaseName):
        self.__databaseName = databaseName

        self.__db = mysql.connect(
            host="localhost",
            user="python",
            passwd="Python123"
        )

        self.__cursor = self.__db.cursor()

    # endregion

    # region 2. Create Database

    def createDatabase(self):
        try:
            self.__cursor.execute("CREATE DATABASE " + self.__databaseName)

        except:
            pass

        self.__db = mysql.connect(
            host="localhost",
            user="python",
            passwd="Python123",
            database=self.__databaseName
        )

        self.__cursor = self.__db.cursor()

    # endregion

    # region 3. Create Table

    def createTable(self):
        try:
            self.__cursor.execute(
                "CREATE TABLE weights (nId1 INTEGER, nId2 INTEGER, weight DOUBLE)"
            )
        except:
            pass

    # endregion

    # region 4. Insert to the table

    def insertToTheTable(self, nId1, nId2, weight=0):
        row = (nId1, nId2, weight)
        self.__cursor.execute("INSERT INTO weights (nId1, nId2, weight) VALUES (%s, %s, %s)", row)

        self.__db.commit()

    # endregion

    # region 5. Getters values from table

    def getWeightByTwoNeuronId(self, nId1, nId2):
        self.__cursor.execute("SELECT weight FROM weights WHERE nId1=" + str(nId1) + " AND nId2=" + str(nId2))

        weight = self.__cursor.fetchone()
        floatWeight = float(weight[0])
        return floatWeight

    def getRowsSize(self):
        try:
            self.__cursor.execute("SELECT * FROM weights")
            rows = self.__cursor.fetchall()
            return len(rows)
        except:
            return 0

    # endregion

    # region 6. Update values at the table

    def setWeightByTwoNeuronId(self, nId1, nId2, newWeight):
        self.__cursor.execute("UPDATE weights SET weight=" + str(newWeight) + "WHERE nId1=" + str(nId1) + " AND nId2=" + str(nId2))

        self.__db.commit()

    # endregion

    # region 7. Delete table

    def deleteTable(self):
        self.__cursor.execute("DROP TABLE weights")

        self.__db.commit()

    # endregion
