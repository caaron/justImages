import sys
from PyQt5 import QtCore, QtWidgets
import numpy as np
import cv2







if __name__ == "__main__":
    image = cv2.imread("100-Pics-Quiz-Logo-Pack-Answers-1-50.jpg")
#    output = mask(image,0b1100)
#    show(output)
    timedReveal(image)
    print("all done")
