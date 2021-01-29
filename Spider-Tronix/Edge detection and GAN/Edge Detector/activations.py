import numpy as np
alpha = 0.02
def relu(matrix):
    return np.where(matrix > 0, matrix, 0)
def sigmoid(matrix):
    return 1/(1+np.exp(-matrix))
def leakyRelu(matrix):
    return np.where(matrix>0, matrix, alpha*matrix)
