import cv2
import numpy as np

def display(x):
    pass
loc = input("enter the location of your image ")

img = cv2.imread(loc)
cv2.namedWindow('filter')
cv2.createTrackbar('R','filter', 0, 255, display)
cv2.createTrackbar('G','filter', 0, 255, display)
cv2.createTrackbar('B','filter', 0, 255, display)

while 1:
    r = cv2.getTrackbarPos('R','filter' )
    g = cv2.getTrackbarPos('G','filter' )
    b = cv2.getTrackbarPos('B','filter' )
    final = np.where(img == [b,g,r], img, np.zeros(np.shape(img)))


    cv2.imshow('filter', final)
    k = cv2.waitKey(1) & 0xFF
    if k ==27:
        break

cv2.destroyAllWindows()
