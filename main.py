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
        #self.conn = sqlite3.connect('faceDatabase.db')
        #self.c = self.conn.cursor()
        #self.createTable()
        #self.dynamicDataEntry()
        #self.readFromDB()



    def createTable(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS people(Id REAL, name TEXT)')


    def dynamicDataEntry(self):
        self.userId = 5
        self.userName = "Felipe"
        self.c.execute("INSERT INTO people (Id,name) VALUES(?,?)", (self.userId, self.userName))
        self.conn.commit()


    def readFromDB(self):
        self.c.execute("SELECT * FROM people Where Id = 0")
        for row in self.c.fetchall():
            print(row)

        self.createOrUpdate(10,"Pedro")


    def createOrUpdate(self,Id,name):
        self.c.execute("SELECT * FROM people WHERE Id = ?", (Id,))
        ifRecordExist = False
        for row in self.c.fetchall():
            ifRecordExist = True
        if (ifRecordExist == True):
            self.c.execute("UPDATE people SET name= ?  WHERE Id = ?", (name,Id))
        else:
            self.c.execute("INSERT INTO people (Id,name) Values(?,?)", (Id, name))

        self.conn.commit()


    def getProfile(self,Id):
        self.c.execute("SELECT * FROM people WHERE Id = ?", (Id,))
        profile = None
        for row in self.c.fetchall():
            profile = row
            print(row)
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

        # Detect Faces
        for (x, y, w, h) in self.faces:
            cv2.rectangle(self.imageDetection, (x, y), (x + w, y + h), (225, 0, 0), 2)

            gray = cv2.cvtColor(self.imageDetection, cv2.COLOR_BGR2GRAY)
            self.faces = self.faceCascade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in self.faces:
                cv2.rectangle(self.imageDetection, (x, y), (x + w, y + h), (225, 0, 0), 2)
                [Id, conf] = self.recognizer.predict(gray[y:y + h, x:x + w])
                if (conf > 50):
                    if (Id == 1):
                        Id = "Felipe"
                    elif (Id == 2):
                        Id = "Elder Bednar"
                else:
                    Id = "Unknown"
                cv2.putText(self.imageDetection, str(Id), (x, y + h), self.fontface, self.fontscale, self.fontcolor)

                # Predict returns an Id and confidence value
            #[Id,conf] = self.recognizer.predict(self.gray[y:y + h, x:x + w])

            #self.profile = self.getProfile(self.idUser)
            #if (self.profile != None and conf > 50):
             #   cv2.putText(self.imageDetection, str(self.profile[1]), (x, y + h), self.fontface, self.fontscale, self.fontcolor)
            #else:
             #   Id = "Unknown"
              #  cv2.putText(self.imageDetectionim, str(Id), (x, y + h), self.fontface, self.fontscale, self.fontcolor)




            #if (conf > 50):
             #   if (Id == 1):
              #      Id = "Felipe"
               # elif (Id == 2):
                #    Id = "Elder Bednar"
            #else:
             #   Id = "Unknown"
            #cv2.putText(self.imageDetection, str(Id), (x, y + h), self.fontface,
             #           self.fontscale, self.fontcolor)

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
