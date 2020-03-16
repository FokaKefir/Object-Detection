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
        self.__newImg = self.__img[ymin:ymax, xmin:xmax]

    def resizeImg(self, w, h):
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

    # endregion
