import cv2
import numpy as np
import PyQt5
import sys
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class FaceDetection(QDialog):
    def __init__(self):
        super(FaceDetection, self).__init__()
        loadUi('faceDetection.ui',self)

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainner/trainner.yml')
        self.cascadePath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)
        self.Id = 0

        self.fontface = cv2.FONT_HERSHEY_SIMPLEX
        self.fontscale = 1
        self.fontcolor = (0, 0, 255)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        # Initialize  BuToons and label
        self.image = None
        self.imageDetection = None
        self.start.clicked.connect(self.startCam)
        self.stop.clicked.connect(self.stopCam)
        self.startCam()

    @pyqtSlot()
    def startCam(self):

        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,640)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(5) # while 5 milisecond is going to call updateFrame()

    def updateFrame(self):
        ret, self.image = self.cam.read()
        ####################
        ret, self.imageDetection = self.cam.read()
        self.gray = cv2.cvtColor(self.imageDetection, cv2.COLOR_BGR2GRAY)
        self.faces = self.faceCascade.detectMultiScale(self.gray, 1.2, 5)
        ####################

        self.image = cv2.flip(self.image,1)
        self.displayVideo(self.image,1)

    def stopCam(self):
        self.timer.stop()

    def displayVideo(self,image,window=1):
        qformat = QImage.Format_Indexed8
        if len(image.shape)==3: # Shape
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        outVideo = QImage(image,image.shape[1],image.shape[0],image.strides[0],qformat)
        outVideo = outVideo.rgbSwapped()

        #############################
        for (x, y, w, h) in self.faces:
            cv2.rectangle(self.imageDetection, (x, y), (x + w, y + h), (225, 0, 0), 2)
            [Id, conf] = self.recognizer.predict(self.gray[y:y + h, x:x + w])
            if (conf > 50):
                if (Id == 1):
                    Id = "Felipe"
                elif (Id == 2):
                    Id = "Elder Bednar"
            else:
                Id = "Unknown"
            cv2.putText(self.imageDetection, str(Id), (x, y + h), self.fontface,
                        self.fontscale, self.fontcolor)

        #################################
        if window == 1:
            self.frameVideo.setPixmap(QPixmap.fromImage(outVideo))
            self.frameVideo.setScaledContents(True)


app = QApplication(sys.argv)
window = FaceDetection()
window.setWindowTitle('Face Detection')
window.show()
sys.exit(app.exec_())
