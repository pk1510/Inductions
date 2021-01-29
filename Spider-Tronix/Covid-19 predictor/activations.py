import numpy as np
import math

def activation(matrix, THETA):
    matrix.astype(np.float64)
    return 1.0/(1.0 + np.exp(-np.dot(matrix, THETA.transpose()), dtype=np.float64, casting='unsafe'))
