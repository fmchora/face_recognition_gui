import cv2
import numpy
import PyQt5
img = cv2.imread('goku.png',1)
cv2.imshow('goku',img)
cv2.waitKey()
cv2.destroyAllWindows()
