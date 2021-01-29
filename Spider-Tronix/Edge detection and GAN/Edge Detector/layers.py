''' only the layers 1,2,8,9,10 are used. self_padding is not used. but i used that variable elsewhere, so the input matrix is not padded. I didnt use
self.normed in fc layers since sigmoid itself outputs values between 0 and 1. i didnt use self.location, instead i used self.mask to keep track of my maximum
values while pooling. i used leaky relu activation function in my conv layers. adding bias ie, 1 to each and every eleemnt gave me a horizontal loss vs epochs
graph so i din use that.. i think that was because 1 was very large compared to the values which i get during my computation, so no effect in gradient descent
i used epsilon to prevent zero standard deviation. i used pool of size 2 for second layer and pool of size 3 for first layer without any stride and 2x3x3, 4x3x3 filters with  max pooling'''



import cv2
import numpy as np
import activations
epsilon = 10**(-20)

class layer1:
    def __init__(self,matrix,filter):
        self.weights = filter
        #self.padding = self.__padding__(matrix)
        self.padding = matrix
        self.norm = self.__batchNorm__(self.padding)
        self.convolving = self.__convolve__(self.norm, self.weights)
        #self.activated = activations.relu(self.convolving)

        #self.activated = activations.sigmoid(self.convolving+1)
        self.activated = activations.leakyRelu(self.convolving)
        self.final, self.indices, self.mask = self.__maxPool__(self.activated)
        self.err_input = np.zeros(np.shape(matrix))
        self.err_filter = np.zeros(np.shape(self.weights))
    def __padding__(self,matrix):
        return np.pad(matrix,((0,0), (0,0), (1,1), (1,1)), constant_values=(0,0))

    def __convolve__(self,matrix,filter):
        result = np.zeros((np.size(matrix,0),2, np.size(matrix,2)-2,np.size(matrix,3)-2 ))
        for l in range(0,np.size(result,1)):
            for i in range(0,1000):
                for j in range(0,np.size(result,2)):
                    for k in range(0,np.size(result,3)):
                        result[i,l,j,k] = np.sum(np.multiply(matrix[i,:,j:j+3,k:k+3], filter[l]))

        return result
    def __batchNorm__(self, matrix):
        self.mean = np.mean(matrix, axis=0)
        self.std = np.std(matrix, axis=0)
        return (matrix-self.mean)/(self.std + epsilon)

    def __maxPool__(self,matrix):
        pooled = np.zeros((np.size(matrix,0), 2, np.size(matrix,2)-2, np.size(matrix,3)-2))
        self.imSize = np.size(pooled,3)
        mask = np.zeros(np.shape(matrix))
        location = {0: [], 1: []}
        for i in range(0,1000):
            for l in range(0,np.size(pooled,1)):
                for j in range(0,np.size(pooled,2)):
                    for k in range(0,np.size(pooled,3)):
                        pooled[i,l,j,k] = np.amax(matrix[i,l,j:j+3,k:k+3])
                        location[l].append(np.where(matrix[i,l,j:j+3,k:k+3] == pooled[i,l,j,k]))
                        mask[i,l,j:j+3,k:k+3] += np.where(matrix[i,l,j:j+3,k:k+3] == pooled[i,l,j,k], 1, 0)     # since i am using stride=1, this code may give 0 to my previous found max.
                        mask[i,l,j:j+3,k:k+3] = np.where(mask[i,l,j:j+3,k:k+3] == 2, 1, mask[i,l,j:j+3,k:k+3])  # so i add it.. and if i get something as 2, this means it is the max for 2 convolutions. so we make it 1 leaving others undisturbed
        return pooled, location, mask
class layer2:
    def __init__(self,matrix,filter):
        self.weights = filter
        #self.padding = self.__padding__(matrix)
        self.padding = matrix                                          #NO padding, input is of size 2x4x4, output will be 4x1x1, since pooling of size 2 is used
        self.norm = self.__batchNorm__(self.padding)
        self.convolving = self.__convolve__(self.norm, self.weights)

        self.activated = activations.leakyRelu(self.convolving)
        #self.activated = activations.sigmoid(self.convolving+1)
        #self.activated = activations.relu(self.convolving)
        self.final, self.indices, self.mask = self.__maxPool__(self.activated)
        self.err_input = np.zeros(np.shape(matrix))
        self.err_filter = np.zeros(np.shape(self.weights))
    def __padding__(self,matrix):
        return np.pad(matrix,((0,0), (0,0), (1,1), (1,1)), constant_values=(0,0))

    def __convolve__(self,matrix,filter):
        result = np.zeros((np.size(matrix,0),4, np.size(matrix,2)-2,np.size(matrix,3)-2 ))
        for l in range(0,np.size(result,1)):
            for i in range(0,1000):
                for j in range(0,np.size(result,2)):
                    for k in range(0,np.size(result,3)):
                        result[i,l,j,k] = np.sum(np.multiply(matrix[i,:,j:j+3,k:k+3], filter[l]))

        return result
    def __batchNorm__(self, matrix):
        self.mean = np.mean(matrix, axis=0)
        self.std = np.std(matrix, axis=0)
        return (matrix-self.mean)/(self.std + epsilon)
    def __maxPool__(self,matrix):
        pooled = np.zeros((np.size(matrix,0), 4, np.size(matrix,2)-1, np.size(matrix,3)-1))
        self.imSize = np.size(pooled,3)
        mask = np.zeros(np.shape(matrix))
        location = {0: [], 1: [], 2: [], 3: []}                                           #mask is used indstead of this
        for i in range(0,1000):
            for l in range(0,np.size(pooled,1)):
                for j in range(0,np.size(pooled,2)):
                    for k in range(0,np.size(pooled,3)):
                        pooled[i,l,j,k] = np.amax(matrix[i,l,j:j+2,k:k+2])
                        location[l].append(np.where(matrix[i,l,j:j+2,k:k+2] == pooled[i,l,j,k]))
                        mask[i,l,j:j+2,k:k+2] += np.where(matrix[i,l,j:j+2,k:k+2] == pooled[i,l,j,k], 1, 0)
                        mask[i,l,j:j+2,k:k+2] = np.where(mask[i,l,j:j+2,k:k+2] == 2, 1, mask[i,l,j:j+2,k:k+2])
        return pooled, location, mask

'''class layer3:
    def __init__(self,matrix,filter):
        self.weights = filter
        self.padding = self.__padding__(matrix)
        convolving = self.__convolve__(self.padding, self.weights)
        convolving_norm = self.__batchNorm__(convolving)
        #self.activated = activations.relu(convolving + 1)
        #self.activated = activations.sigmoid(convolving_norm+1)
        self.activated = activations.leakyRelu(convolving+1)
        self.final, self.indices = self.__maxPool__(self.activated)
        self.err_input = np.zeros(np.shape(matrix))
        self.err_filter = np.zeros(np.shape(self.weights))

    def __padding__(self,matrix):
        return np.pad(matrix,((0,0), (0,0), (1,1), (1,1)), constant_values=(0,0))

    def __convolve__(self,matrix,filter):
        result = np.zeros((np.size(matrix,0),6, np.size(matrix,2)-2,np.size(matrix,3)-2 ))

        for l in range(0,np.size(result,1)):

            for i in range(0,1000):
                for j in range(0,np.size(result,2)):
                    for k in range(0,np.size(result,3)):
                        result[i,l,j,k] = np.sum(np.multiply(matrix[i,:,j:j+3,k:k+3], filter[l]))

        return result
    def __batchNorm__(self, matrix):
        self.mean = np.mean(matrix, axis=0)
        self.std = np.std(matrix, axis=0)
        return (matrix-self.mean)/(self.std + epsilon)

    def __maxPool__(self,matrix):
        pooled = np.zeros((np.size(matrix,0), 6, np.size(matrix,2)-2, np.size(matrix,3)-2))
        self.imSize = np.size(pooled,3)
        location = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
        for i in range(0,1000):
            for l in range(0,np.size(pooled,1)):
                for j in range(0,np.size(pooled,2)):
                    for k in range(0,np.size(pooled,3)):
                        pooled[i,l,j,k] = np.amax(matrix[i,l,j:j+3,k:k+3])
                        location[l].append(np.where(matrix[i,l,j:j+3,k:k+3] == pooled[i,l,j,k]))
        return pooled, location

class layer4:
    def __init__(self,matrix,filter):
        self.weights = filter
        self.padding = self.__padding__(matrix)
        convolving = self.__convolve__(self.padding, self.weights)
        convolving_norm = self.__batchNorm__(convolving)
        #self.activated = activations.relu(convolving + 1)
        #self.activated = activations.sigmoid(convolving_norm+1)
        self.activated = activations.leakyRelu(convolving+1)
        self.final, self.indices = self.__maxPool__(self.activated)
        self.err_input = np.zeros(np.shape(matrix))
        self.err_filter = np.zeros(np.shape(self.weights))
    def __padding__(self,matrix):
        return np.pad(matrix,((0,0), (0,0), (1,1), (1,1)), constant_values=(0,0))

    def __convolve__(self,matrix,filter):
        result = np.zeros((np.size(matrix,0),8, np.size(matrix,2)-2,np.size(matrix,3)-2 ))

        for l in range(0,np.size(result,1)):

            for i in range(0,1000):
                for j in range(0,np.size(result,2)):
                    for k in range(0,np.size(result,3)):
                        result[i,l,j,k] = np.sum(np.multiply(matrix[i,:,j:j+3,k:k+3], filter[l]))

        return result
    def __batchNorm__(self, matrix):
        self.mean = np.mean(matrix, axis=0)
        self.std = np.std(matrix, axis=0)
        return (matrix-self.mean)/(self.std + epsilon)
    def __maxPool__(self,matrix):
        pooled = np.zeros((np.size(matrix,0), 8, np.size(matrix,2)-2, np.size(matrix,3)-2))
        self.imSize = np.size(pooled,3)
        location = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        for i in range(0,1000):
            for l in range(0,np.size(pooled,1)):
                for j in range(0,np.size(pooled,2)):
                    for k in range(0,np.size(pooled,3)):
                        pooled[i,l,j,k] = np.amax(matrix[i,l,j:j+3,k:k+3])
                        location[l].append(np.where(matrix[i,l,j:j+3,k:k+3] == pooled[i,l,j,k]))
        return pooled, location

class layer5:
    def __init__(self,matrix,filter):
        self.weights = filter
        self.padding = self.__padding__(matrix)
        convolving = self.__convolve__(self.padding, self.weights)
        convolving_norm = self.__batchNorm__(convolving)
        #self.activated = activations.relu(convolving + 1)
        #self.activated = activations.sigmoid(convolving_norm+1)
        self.activated = activations.leakyRelu(convolving+1)
        self.final, self.indices = self.__maxPool__(self.activated)
        self.err_input = np.zeros(np.shape(matrix))
        self.err_filter = np.zeros(np.shape(self.weights))
    def __padding__(self,matrix):
        return np.pad(matrix,((0,0), (0,0), (1,1), (1,1)), constant_values=(0,0))

    def __convolve__(self,matrix,filter):
        result = np.zeros((np.size(matrix,0),10, np.size(matrix,2)-2,np.size(matrix,3)-2 ))

        for l in range(0,np.size(result,1)):

            for i in range(0,1000):
                for j in range(0,np.size(result,2)):
                    for k in range(0,np.size(result,3)):
                        result[i,l,j,k] = np.sum(np.multiply(matrix[i,:,j:j+3,k:k+3], filter[l]))

        return result
    def __batchNorm__(self, matrix):
        self.mean = np.mean(matrix, axis=0)
        self.std = np.std(matrix, axis=0)
        return (matrix-self.mean)/(self.std + epsilon)
    def __maxPool__(self,matrix):
        pooled = np.zeros((np.size(matrix,0), 10, np.size(matrix,2)-1, np.size(matrix,3)-1))
        self.imSize = np.size(pooled, 3)
        location = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
        for i in range(0,1000):
            for l in range(0,np.size(pooled,1)):
                for j in range(0,np.size(pooled,2)):
                    for k in range(0,np.size(pooled,3)):
                        pooled[i,l,j,k] = np.amax(matrix[i,l,j:j+2,k:k+2])
                        location[l].append(np.where(matrix[i,l,j:j+2,k:k+2] == pooled[i,l,j,k]))
        return pooled, location

class layer6:
    def __init__(self,matrix,THETA):
        self.input = np.hstack((np.ones((np.size(matrix, 0), 1)), matrix))
        self.mean = np.mean(matrix, axis=0)
        self.std = np.std(matrix, axis=0, dtype=np.float64)
        matrix_normed = (matrix-self.mean)/self.std
        biased = np.hstack((np.ones((np.size(matrix,0), 1)), matrix_normed))
        self.biased = biased
        self.THETA = THETA
        z = np.dot(self.input, self.THETA.transpose())
        self.final = activations.sigmoid(z)
        self.resnet = matrix


class layer7:
    def __init__(self,matrix,resnet,THETA):  # this matrix shld be self.resnet
        self.input = np.hstack((np.ones((np.size(matrix, 0), 1)), matrix))
        self.mean = np.mean(matrix, axis=0)
        self.std = np.std(matrix, axis=0, dtype=np.float64)
        matrix_normed = (matrix-self.mean)/self.std
        biased = np.hstack((np.ones((np.size(matrix,0),1)), matrix_normed))
        self.biased = biased
        self.THETA = THETA
        z = np.dot(self.input, self.THETA.transpose())
        self.final = activations.sigmoid(z+resnet)'''
class layer8:
    def __init__(self,matrix,THETA):
        self.input = np.hstack((np.ones((np.size(matrix, 0), 1)), matrix))
        #self.mean = np.mean(matrix, axis=0)
        #self.std = np.std(matrix, axis=0, dtype=np.float64)
        #matrix_normed = (matrix-self.mean)/(self.std+epsilon)
        #biased = np.hstack((np.ones((np.size(matrix,0),1)), matrix_normed))
        #self.biased = biased                                                       #seld.biased is not used in fcs
        self.THETA = THETA
        z = np.dot(self.input, self.THETA.transpose())
        self.final = activations.sigmoid(z)
class layer9:
    def __init__(self,matrix,THETA):
        self.input = np.hstack((np.ones((np.size(matrix, 0), 1)), matrix))
        #self.mean = np.mean(matrix, axis=0)
        #self.std = np.std(matrix, axis=0, dtype=np.float64)
        #matrix_normed = (matrix-self.mean)/(self.std+epsilon)
        #biased = np.hstack((np.ones((np.size(matrix,0),1)), matrix_normed))
        #self.biased = biased
        self.THETA = THETA
        z = np.dot(self.input, self.THETA.transpose())
        self.final = activations.sigmoid(z)
class layer10:
    def __init__(self,matrix,THETA):
        self.input = np.hstack((np.ones((np.size(matrix, 0), 1)), matrix))
        #self.mean = np.mean(matrix, axis=0)
        #self.std = np.std(matrix, axis=0, dtype=np.float64)
        #matrix_normed = (matrix-self.mean)/(self.std+epsilon)
        #biased = np.hstack((np.ones((np.size(matrix,0),1)), matrix_normed))
        #self.biased = biased
        self.THETA = THETA
        z = np.dot(self.input, self.THETA.transpose())
        self.final = activations.sigmoid(z)
