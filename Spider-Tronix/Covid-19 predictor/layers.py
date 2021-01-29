import numpy as np

class layer1:
    def __init__(self, matrix):
        self.mean = np.mean(matrix, axis=0)
        self.std = np.std(matrix, axis = 0, dtype=np.float32)
        self.z = np.hstack((np.ones((np.size(matrix, 0), 1)),self.__featureNormalize(matrix)))
    def __featureNormalize(self, matrix):
        means = np.tile(self.mean, (np.size(matrix, 0),1))
        stds = np.tile(self.std, (np.size(matrix, 0),1))
        return np.divide(matrix-means, stds)

class layer2:
    def __init__(self, matrix1, matrix2):
        self.mean = np.mean(np.hstack((matrix1, matrix2)), axis=0)
        self.std = np.std(np.hstack((matrix1, matrix2)), axis = 0, dtype=np.float32)
        self.z = np.hstack((np.ones((np.size(matrix1, 0), 1)),self.__featureNormalize(np.hstack((matrix1, matrix2)))))
    def __featureNormalize(self, matrix):
        means = np.tile(self.mean, (np.size(matrix, 0),1))
        stds = np.tile(self.std, (np.size(matrix, 0),1))
        return np.divide(matrix-means, stds)

class layer3:
    def __init__(self, matrix):
        self.mean = np.mean(matrix, axis=0)
        self.std = np.std(matrix, axis = 0, dtype=np.float32)
        self.z = np.hstack((np.ones((np.size(matrix, 0), 1)),self.__featureNormalize(matrix)))
    def __featureNormalize(self, matrix):
        means = np.tile(self.mean, (np.size(matrix, 0),1))
        stds = np.tile(self.std, (np.size(matrix, 0),1))
        return np.divide(matrix-means, stds)

class layer4:
    def __init__(self, matrix):
        self.mean = np.mean(matrix, axis=0)
        self.std = np.std(matrix, axis = 0, dtype=np.float32)
        self.z = np.hstack((np.ones((np.size(matrix, 0), 1)),self.__featureNormalize(matrix)))
    def __featureNormalize(self, matrix):
        means = np.tile(self.mean, (np.size(matrix, 0),1))
        stds = np.tile(self.std, (np.size(matrix, 0),1))
        return np.divide(matrix-means, stds)

class layer5:
    def __init__(self, matrix):
        self.mean = np.mean(matrix, axis=0)
        self.std = np.std(matrix, axis = 0, dtype=np.float32)
        self.z = self.__featureNormalize(matrix)
    def __featureNormalize(self, matrix):
        means = np.tile(self.mean, (np.size(matrix, 0),1))
        stds = np.tile(self.std, (np.size(matrix, 0),1))
        return np.divide(matrix-means, stds)
