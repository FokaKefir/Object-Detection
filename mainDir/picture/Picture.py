import cv2
import numpy as np

FRAME = 0
WALL = -1

IMG_SIZE = (500, 500)

class Picture:

    # region 1. Init Object

    def __init__(self, img = None, w=None, h=None):
        self.__img = cv2.resize(img, IMG_SIZE)
        self.__newImg = img
        self.__width = w
        self.__height = h

        self.__boxes = []

    # endregion

    # region 2. Crop the image

    def cropImg(self, xmin, ymin, xmax, ymax):
        self.__newImg = self.__img[ymin:ymax, xmin:xmax]

    def resizeNewImg(self, w, h):
        dim = (w, h)
        self.__newImg = cv2.resize(self.__newImg, dim)

    def calculatingInput(self):
        inputList = []

        for row in self.__newImg:
            nRow = []
            for i in range(len(row)):
                nRow.append(float(row[i] / 255))
            inputList.extend(nRow)

        return inputList

    def resizeImg(self, img, w=None, h=None, dim=None):
        if dim is None:
            dim = (w, h)
        img = cv2.resize(img, dim)
        return img

    # endregion

    # region 3. Calculating boxes

    def getBoxes(self):
        self.imageFrame()
        return self.__boxes

    def setWalls(self, mat, imgCont, dim):
        row, col = dim
        for i in range(row):
            for j in range(col):
                if imgCont[i][j] == FRAME:
                    mat[i][j] = WALL

    def lookNeight(self, mat, dim, poz, l):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        maxRow, maxCol = dim
        row, col = poz
        maxi = poz
        mini = poz
        for dir in directions:
            r = row + dir[0]
            c = col + dir[1]
            if r < 0 or c < 0 or r >= maxRow or c >= maxCol:
                continue

            elif mat[r][c] == 0:
                mat[r][c] = mat[row][col]

                if maxi[0] < r or maxi[1] < c:
                    maxi = (r, c)
                if r < mini[0] or c < mini[1]:
                    mini = (r, c)

                l.append((r, c))

        return (maxi, mini)

    def lee(self, mat, dim, poz, index):
        l = []
        l.append(poz)
        r, c = poz
        maxi = poz
        mini = poz
        mat[r][c] = index
        while len(l):
            actPoz = l.pop(0)
            newMaxi, newMini = self.lookNeight(mat, dim, poz=actPoz, l=l)
            if newMaxi[0] > maxi[0]:
                maxi = (newMaxi[0], maxi[1])
            if newMaxi[1] > maxi[1]:
                maxi = (maxi[0], newMaxi[1])

            if newMini[0] < mini[0]:
                mini = (newMini[0], mini[1])
            if newMini[1] < mini[1]:
                mini = (mini[0], newMini[1])

        return (mini, maxi)

    def calcObjects(self, imgCont):
        row, col = IMG_SIZE

        mat = [[0] * (col+1) for _ in range(row+1)]
        self.setWalls(mat, imgCont, (row, col))

        index = 1

        for i in range(row):
            for j in range(col):
                if mat[i][j] == 0:
                    start, end = newBox = self.lee(mat, (row, col), (i, j), index)

                    size = (end[0] - start[0]) * (end[1] - start[1])
                    if size > (IMG_SIZE[0] * IMG_SIZE[1]) * (5/100):
                        self.__boxes.append(newBox)

                    index += 1

    def imageFrame(self):
        img = self.__img

        img = self.resizeImg(img, dim=IMG_SIZE)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img, 150, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        imgContours = cv2.drawContours(img, contours, -1, FRAME, 7)

        self.calcObjects(imgContours)

    def rectangleBoxes(self, image=None):
        if image is None:
            image = self.__img

        for box in self.__boxes:
            start, end = box
            start = (start[1], start[0])
            end = (end[1], end[0])
            image = cv2.rectangle(image, start, end, (255, 0, 0), 2)

    # endregion

    # region 4. Open image

    def showMatrix(self, mat, row, col):
        img = self.__img
        for i in range(row):
            for j in range(col):
                if mat[i][j] == -1:
                    img[i][j] = 0
                else:
                    img[i][j] = mat[i][j]
                img[i][j] = img[i][j] * 10

        self.rectangleBoxes(image=img)
        self.showImg(img)

    def showImg(self, img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)

    # endregion
