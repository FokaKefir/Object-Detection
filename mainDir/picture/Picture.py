import cv2
import numpy as np


class Picture:

    # region 1. Init Object

    def __init__(self, img, w, h):
        self.__img = img
        self.__width = w
        self.__height = h

    # endregion

    # region 2. Crop the image

    def cropImg(self, xmin, ymin, xmax, ymax):
        row = xmax - xmin + 1
        col = ymin - ymax + 1
        self.__newImg = [[0] * col] * row
        for i in range(xmin, xmax+1):
            for j in range(ymin, ymax+1):
                self.__newImg[i - xmin][j - ymin] = self.__img[i][j]

    def calculatingInput(self):
        inputList = []

        for row in self.__newImg:
            inputList.extend(row)

        return inputList

    # endregion
