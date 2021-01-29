import numpy as np
import activations
import layers


def fNorm(matrix):
    means = np.tile(np.mean(matrix, axis=0), (np.size(matrix, 0),1))
    stds = np.tile(np.std(matrix, axis=0, dtype=np.float32), (np.size(matrix, 0),1))
    return np.divide(matrix-means, stds), means[0,:], stds[0,:]      #''' returning mean and std of each columns'''

def forBackprop(matrix1, matrix2, Y, Theta1, Theta2, Theta3, Theta4, Lambda): # forward and back prop to predict the cost fn and its derivatives
    z1 = activations.activation(matrix1, Theta1)
    #z1Normed, meanz1, stdz1 = featureNormalize.fNorm(np.hstack((z1, matrix2)))
    #z1_ = np.hstack((np.ones((np.size(matrix1, 0), 1)), z1Normed))
    a2 = layers.layer2(z1, matrix2)

    z2 = activations.activation(a2.z, Theta2)
    #z2Normed, meanz2, stdz2 = featureNormalize.fNorm(z2)
    #z2_ = np.hstack((np.ones((np.size(matrix1, 0), 1)),z2Normed))
    a3 = layers.layer3(z2)
    z3 = activations.activation(a3.z, Theta3)
    #z3Normed, meanz3, stdz3 = featureNormalize.fNorm(z3)
    #z3_ = np.hstack((np.ones((np.size(matrix1, 0), 1)),z3Normed))
    a4 = layers.layer4(z3)
    z4 = activations.activation(a4.z, Theta4) #hypothesis

    m = np.size(matrix1, 0)
    J = (np.trace(np.dot((z4 - Y).transpose(), z4 - Y)) + Lambda*(np.sum(np.square(Theta1[:,1:]), axis=None) + np.sum(np.square(Theta2[:,1:]), axis=None) + np.sum(np.square(Theta3[:,1:]), axis=None) + np.sum(np.square(Theta4[:,1:]), axis=None) ))/(2*m)
    #backprop

    del2 = np.zeros((9,1))                         #the derivative of the input values is 0 . so the last 4 is 0
    del5 = (z4 - Y).transpose()                    # while multiplying with data matrix we get row vector ..so we take transpose
    del4 = np.multiply(np.dot(Theta4[:,1:].transpose(), del5), (np.multiply(a4.z[:,1:], np.ones(np.shape(a4.z[:,1:])) - a4.z[:,1:])).transpose())
    del3 = np.multiply(np.dot(Theta3[:,1:].transpose(), del4), (np.multiply(a3.z[:,1:], np.ones(np.shape(a3.z[:,1:])) - a3.z[:,1:])).transpose())
    del2 = np.multiply(np.dot(Theta2[:,1:6].transpose(), del3), (np.multiply(a2.z[:,1:6], np.ones(np.shape(a2.z[:,1:6])) - a2.z[:,1:6])).transpose()) # remaining dow / dow z is 0 as it is an input value

    '''tri_1 = np.zeros((5,3))
    tri_2 = np.zeros((7,10))
    tri_3 = np.zeros((5,8))
    tri_4 = np.zeros((2,6))'''

    tri_1 = (np.dot(del2, matrix1[:,1:]) + Lambda*(Theta1[:,1:]))/m
    tri_2 = (np.dot(del3, a2.z[:,1:]) + Lambda*(Theta2[:,1:]))/m
    tri_3 = (np.dot(del4, a3.z[:,1:]) + Lambda*(Theta3[:, 1:]))/m
    tri_4 = (np.dot(del5, a4.z[:,1:]) + Lambda*(Theta4[:, 1:]))/m
    return z4, J, tri_1, tri_2, tri_3, tri_4, a2.mean, a2.std, a3.mean, a3.std, a4.mean, a4.std

def costTest(matrix1, matrix2, Y, Theta1, Theta2, Theta3, Theta4):  #''' to find the regularization term'''
    z1 = activations.activation(matrix1, Theta1)
    #z1Normed, meanz1, stdz1 = featureNormalize.fNorm(np.hstack((z1, matrix2)))
    #z1_ = np.hstack((np.ones((np.size(matrix1, 0), 1)), z1Normed))
    a2 = layers.layer2(z1, matrix2)

    z2 = activations.activation(a2.z, Theta2)
    #z2Normed, meanz2, stdz2 = featureNormalize.fNorm(z2)
    #z2_ = np.hstack((np.ones((np.size(matrix1, 0), 1)),z2Normed))
    a3 = layers.layer3(z2)
    z3 = activations.activation(a3.z, Theta3)
    #z3Normed, meanz3, stdz3 = featureNormalize.fNorm(z3)
    #z3_ = np.hstack((np.ones((np.size(matrix1, 0), 1)),z3Normed))
    a4 = layers.layer4(z3)
    z4 = activations.activation(a4.z, Theta4) #hypothesis
    m = np.size(matrix1, 0)
    J = (np.trace(np.dot((z4 - Y).transpose(), z4 - Y)) + Lambda*(np.sum(np.square(Theta1[:,1:]), axis=None) + np.sum(np.square(Theta2[:,1:]), axis=None) + np.sum(np.square(Theta3[:,1:]), axis=None) + np.sum(np.square(Theta4[:,1:]), axis=None) ))/(2*m)
    return J
