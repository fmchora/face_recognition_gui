import cv2
import numpy as np
import PyQt5
import sys

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi




class FaceDetection(QDialog):
    def __init__(self):
        super(FaceDetection, self).__init__()
        loadUi('primero.ui',self)


app = QApplication(sys.argv)
window = FaceDetection()
window.setWindowTitle('Face Detection')
window.show()
sys.exit(app.exec_())
