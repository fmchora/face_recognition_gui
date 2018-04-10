import cv2
import numpy as np
import PyQt5
import sqlite3



import sys
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class FaceDetection(QDialog):
    def __init__(self):
        super(FaceDetection, self).__init__()
        loadUi('faceDetection.ui',self)

        self.conn = sqlite3.connect('faceDatabase.db')
        self.c = self.conn.cursor()

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainner/trainner.yml')
        self.cascadePath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)
        self.Id = 0

        self.fontface = cv2.FONT_HERSHEY_SIMPLEX
        self.fontscale = 1
        self.fontcolor = (0, 0, 255)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        # Initialize  Buttons and label

        self.imageDetection = None
        #self.start.clicked.connect(self.startCam)
        #self.stop.clicked.connect(self.stopCam)
        self.startCam()
        self.createTable()
        self.dynamicDataEntry()

    def createTable(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS people(Id REAL, name TEXT)')


    def dynamicDataEntry(self):
        self.userId = 1
        self.userName = "Felipe"
        self.c.execute("INSERT INTO people (Id,name) VALUES(?,?)", (self.userId, self.userName))
        self.conn.commit()
        self.c.close()
        self.conn.close()

    def readFromDB(self):


    def getProfile(Id):
        pass



        ##connection = sqlite3.connect('faceDatabase.db')
        cmd = "SELECT * FROM people WHERE Id=" + str(Id)
        cursor = connection.execute(cmd)
        profile = None
        for row in cursor:
            profile = row
        connection.close()
        return profile




    @pyqtSlot()
    def startCam(self):

        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,640)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(5) # while 5 mil second is going to call updateFrame()

    def updateFrame(self):
        ret, self.imageDetection = self.cam.read()
        self.gray = cv2.cvtColor(self.imageDetection, cv2.COLOR_BGR2GRAY)
        self.faces = self.faceCascade.detectMultiScale(self.gray, 1.2, 5)

        ## Detect Faces
        for (x, y, w, h) in self.faces:
            cv2.rectangle(self.imageDetection, (x, y), (x + w, y + h), (225, 0, 0), 2)

            ## Predict returns an Id and confidence value
            [Id, conf] = self.recognizer.predict(self.gray[y:y + h, x:x + w])

            self.profile = self.getProfile(Id)
            if (self.profile != None and conf > 50):
                cv2.putText(self.imageDetection, str(self.profile[1]), (x, y + h), self.fontface, self.fontscale, self.fontcolor)
            else:
                Id = "Unknown"
                cv2.putText(self.imageDetectionim, str(Id), (x, y + h), self.fontface, self.fontscale, self.fontcolor)



           ###########################

            if (conf > 50):
                if (Id == 1):
                    Id = "Felipe"
                elif (Id == 2):
                    Id = "Elder Bednar"
            else:
                Id = "Unknown"
            cv2.putText(self.imageDetection, str(Id), (x, y + h), self.fontface,
                        self.fontscale, self.fontcolor)
            #############
        self.displayVideo(self.imageDetection,1)

    def stopCam(self):
        self.timer.stop()

    def displayVideo(self,imageDetection,window=1):
        qformat = QImage.Format_Indexed8
        if len(imageDetection.shape)==3: # Shape
            if imageDetection.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        outVideo = QImage(imageDetection,imageDetection.shape[1],imageDetection.shape[0],imageDetection.strides[0],qformat)
        outVideo = outVideo.rgbSwapped()


        if window == 1:
            self.frameVideo.setPixmap(QPixmap.fromImage(outVideo))
            self.frameVideo.setScaledContents(True)


app = QApplication(sys.argv)
window = FaceDetection()
window.setWindowTitle('Face Detection')
window.show()
sys.exit(app.exec_())
