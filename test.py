from object_detector.ObjectDetector import ObjectDetector
import cv2


def getImage(name):
    return cv2.imread(name)


if __name__ == '__main__':
    objectDetector = ObjectDetector(labelmap="labelmap.xml")
    objectDetector.setupNeuralNetwork()
    objectDetector.loadImage(img=getImage("test_banana.jpg"))
    objectDetector.loadBoxes()
    objectDetector.detectingObjects()
    objectDetector.printAll()