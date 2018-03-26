import cv2
import numpy
import PyQt5
imagage = cv2.imread('goku.png',1)
cv2.imshow('goku',imagage)
cv2.waitKey()
cv2.destroyAllWindows()
