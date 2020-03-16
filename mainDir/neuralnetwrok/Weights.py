import sqlite3
from sqlite3 import Error

class Weights:

    # region 1. Init

    def __init__(self, databaseName):
        self.__databaseName = databaseName

    # endregion


    # region 2. Create Table

    def createTable(self, conn):
        cursor = conn.cursor()

        try:
            cursor.execute('''CREATE TABLE weights 
            (nId1 int, nId2 int, weight double)''')
        except Error as error:
            print(error)

    # endregion

    # region 3. Insert to the table

    def insertToTheTable(self, conn, nId1, nId2, weight=0):
        cursor = conn.cursor()

        newRow = (nId1, nId2, weight)

        cursor.execute("INSERT INTO weights VALUES (?, ?, ?)", newRow)

        conn.commit()

    # endregion

    # region 4. Getters values from table

    def getWeightByTwoNeuronId(self, conn, nId1, nId2):
        cursor = conn.cursor()

        cursor.execute("SELECT weight FROM weights WHERE nId1=" + str(nId1) + " AND nId2=" + str(nId2))

        weight = cursor.fetchone()

        return float(weight[0])


    def getRowsSize(self, conn):
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM weights")

        return len(cursor.fetchall())

    # endregion

    # region 5. Update values at the table

    def setWeightByTwoNeuronId(self, conn, nId1, nId2, newWeight):
        cursor = conn.cursor()

        cursor.execute("UPDATE weights SET weight=" + str(newWeight) + " WHERE nId1=" + str(nId1) + " AND nId2=" + str(nId2))

        conn.commit()

    # endregion

    # region 6. Delete table

    def deleteTable(self, conn):
        cursor = conn.cursor()

        cursor.execute("DROP TABLE weights")

        conn.commit()

# endregion
