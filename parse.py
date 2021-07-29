import sys
from PyQt5 import QtCore, QtWidgets, uic, QtGui
import numpy as np
import cv2
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog

qtCreatorFile = "parseGUI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.OpenFileButton.clicked.connect(self.OpenFilePressed)
        self.imgFilename = None
        self.image = None
        self.textBrowser_vert.setText("195")
        self.textBrowser_horz.setText("150")
        self.maxVstep = 5000
        self.maxHstep = 5000
        self.vUPButton.clicked.connect(self.vUpPressed)
        self.vDownButton.clicked.connect(self.vDownPressed)
        self.hUPButton.clicked.connect(self.hUpPressed)
        self.hDownButton.clicked.connect(self.hDownPressed)




    def OpenFilePressed(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.textBrowser.setText(fileName)
            self.imgFilename = fileName
            self.image = cv2.imread(self.imgFilename)
            self.displayImage(self.image)

    def displayImageQpix(self):
        if self.imgFilename:
            pix = QPixmap(self.imgFilename)
            item = QtWidgets.QGraphicsPixmapItem(pix)
            scene = QtWidgets.QGraphicsScene(self)
            scene.addItem(item)
            self.graphicsView.setScene(scene)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


    def displayImage(self,image):
        if self.imgFilename:
            frame = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            h, w, c = frame.shape
            bytesPerLine = 3 * w
            img = QtGui.QImage(frame, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            #pix = QtGui.QPixmap.fromImage(img)

            pix2 = QPixmap(img)
            item = QtWidgets.QGraphicsPixmapItem(pix2)
            scene = QtWidgets.QGraphicsScene(self)
            scene.addItem(item)
            self.graphicsView.setScene(scene)

    def drawGrid(self,image):
        if self.image.any():
            #draw some lines for the grid
            image2 = image.copy()
            #rows = []
            boxwidth = int(self.textBrowser_vert.toPlainText())
            boxheight = int(self.textBrowser_horz.toPlainText())
            lastCol = self.image.shape[1]
            lastRow = self.image.shape[0]
            # vert lines
            for x in range(0, lastCol, boxwidth):
                cv2.line(image2, (x, 0), (x, lastRow), (0, 255, 0), 2)
            # horz lines
            for y in range(0, lastRow, boxheight):
                cv2.line(image2, (0, y), (lastCol, y), (0, 255, 0), 2)
            return image2


    def displayGrid(self):
        tmp = self.drawGrid(self.image)
        self.displayImage(tmp)

    def vUpPressed(self):
        x = int(self.textBrowser_vert.toPlainText())
        x = x + 1 if ((x+1) < self.maxVstep) else self.maxVstep
        self.textBrowser_vert.setText(str(x))
        self.displayGrid()

    def vDownPressed(self):
        x = int(self.textBrowser_vert.toPlainText())
        x = x - 1 if ((x-1) > 0) else 1
        self.textBrowser_vert.setText(str(x))
        self.displayGrid()

    def hUpPressed(self):
        x = int(self.textBrowser_horz.toPlainText())
        x = x + 1 if ((x+1) < self.maxHstep) else self.maxHstep
        self.textBrowser_horz.setText(str(x))
        self.displayGrid()

    def hDownPressed(self):
        x = int(self.textBrowser_horz.toPlainText())
        x = x - 1 if ((x-1) > 0) else 1
        self.textBrowser_horz.setText(str(x))
        self.displayGrid()

if __name__ == "__main__":
    #image = cv2.imread("100-Pics-Quiz-Logo-Pack-Answers-1-50.jpg")
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
