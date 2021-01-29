import cv2
import numpy as np
lamda = 1
def sigmoidClassifier(matrix, Y):
    #classified = np.where(matrix>=0.5, 1, 0)
    return -np.sum(np.multiply(Y, np.log(matrix)) + np.multiply(1-Y, np.log(1-matrix)))
#def cost2(matrix, Y):
#    return np.sum(np.multiply(1-Y, np.where(matrix <= -1, 0, 1+matrix)))
