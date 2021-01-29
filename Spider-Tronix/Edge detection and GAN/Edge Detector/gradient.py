import numpy as np
alpha = 0.02
def reluGradient(z):
    return np.where(z>0, 1, 0)
def sigmoidGradient(a):
    return np.multiply(a,1-a)
def svmGradient1(matrix, Y):
    return np.sum(np.multiply(Y,np.where(matrix>1, 0, -1)))
def svmGradient2(matrix, Y):
    return np.sum(np.multiply(1-Y, np.where(matrix<-1, 0, 1)))
def leakyReluGradient(z):
    return np.where(z>0, 1, alpha)
