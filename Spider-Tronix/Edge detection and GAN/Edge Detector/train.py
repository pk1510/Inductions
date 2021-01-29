'''
I Used layers 1,2,8,9,10 alone from the layers.py !!! so only the corresponding tags in my weights, gradients, classes and filters are being used
Functions: forwardProp, backProp, backPool, Backconvolution
global variables:  m-number of training samples, init_size-the number of rows/columns for the initial images, filters for conv layers and weights for fc layers
epsilon is used to prevent overflowing of my sigmoid(for eg -1.5 * 10^8 causes overflowing)input[] - to store input images , output[] to store output images, learning rate, epochs, accuracy, cost[] - cost function.
'''
''' my predictions always converged to 0.5. i tried many different ways to execute my algorithm but still i get the same result. i wasnt able to figure out my error'''


import cv2
import numpy as np
import matplotlib.pyplot as plt
import layers
import costfunction
import gradient
m = 1000


#to find error in filter and input. first the derivative wrt activation function is taken.
def Backconvolution(error,a):
    #back_relu = np.multiply(error, gradient.reluGradient(a.activated-1))   #subtract bias units

    back_relu = np.multiply(error, gradient.leakyReluGradient(a.activated))

    err_filter = np.zeros(np.shape(a.weights))
    err_input = np.zeros(np.shape(a.padding))
    cross_180 = np.zeros(np.shape(a.weights))
    for i in range(0,np.size(err_filter, 0)):                                                #convolution between dow l / dow output and the input image
        for j in range(0,np.size(err_filter, 1)):
            cross_180[i,j,:,:] = np.flipud(np.fliplr(a.weights[i,j,:,:]))                    # we flip the filter to perform full convolution afterwards
            for k in range(0,np.size(err_filter, 2)):
                for l in range(0,np.size(err_filter, 3)):
                    err_filter[i,j,k,l] += np.sum(np.multiply(back_relu[:,i,:,:], a.padding[:,j,k:k+np.size(back_relu, 2), l:l+np.size(back_relu, 3)]))
                    #i dint use padding to minimize the number of layers. but i used a.padding everywhere before so.. this is unpadded normal matrix

    p = (np.size(a.weights, 2) > np.size(back_relu, 2))
    q = (np.size(a.weights, 3) > np.size(back_relu, 3))  #since its a square matrix we dont need this
    '''idea: this can be splitted into three regions, 0-min length Rows/columns(filter, error in output); between length of rows/columns of the two, greather than the length of the rows of the two
    so during the first stage, we can index the filter from last(ie using -1), in the second one the full column of the filter will be convolved, third stage is similar to that of the first. since it is a square matrix, operating this on columns is of the same syntax as that of the rows'''
    for i in range(0,m):
        for k in range(0,np.size(cross_180, 1)):
            for l in range(0,np.size(cross_180, 2)+np.size(back_relu, 2) - 1):
                for h in range(0, np.size(cross_180, 3)+ np.size(back_relu, 3) - 1):

                    if(l <= min(np.size(cross_180, 2), np.size(back_relu, 2))-1):
                        if(p==0):
                            if(h<=min(np.size(cross_180, 3), np.size(back_relu, 3))-1):
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,:l+1,:h+1], cross_180[:,k,-1-l : , -1-h :] ))
                            elif(h in range(np.size(cross_180, 3), np.size(back_relu, 3))):
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,:l+1,h-np.size(cross_180, 3)+1:h+1], cross_180[:,k,-1-l:,:]))
                            else:
                                #print("i",i,"k",k,"l",l,"h",h,np.size(back_relu,3),np.size(cross_180,3))
                                #print(np.shape(back_relu[i,:,:l+1,h+1 - np.size(back_relu, 3) - np.size(cross_180, 3):]), np.shape(cross_180[:,k,-1-l:, :np.size(cross_180, 3)+np.size(back_relu, 3)-h-1]))
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,:l+1,h+1 - np.size(back_relu, 3) - np.size(cross_180, 3):], cross_180[:,k,-1-l:, :np.size(cross_180, 3)+np.size(back_relu, 3)-h-1]))
                        else:
                            if(h<=min(np.size(cross_180, 3), np.size(back_relu, 3))-1):
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,:l+1,:h+1], cross_180[:,k,-1-l : , -1-h :] ))
                            elif(h in range(np.size(cross_180, 3), np.size(back_relu, 3))):
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,:l+1,:], cross_180[:,k,-1-l:,-1-h : np.size(back_relu, 3)-1-h]))
                            else:
                                #print(np.shape(back_relu[i,:,:l+1,h+1 - np.size(back_relu, 3) - np.size(cross_180, 3):]), np.shape(cross_180[:,k,-1-l:, :np.size(cross_180, 3)+np.size(back_relu, 3)-h-1]))

                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,:l+1,h+1 - np.size(back_relu, 3) - np.size(cross_180, 3):], cross_180[:,k,-1-l:, :np.size(cross_180, 3)+np.size(back_relu, 3)-h-1]))

                    elif(l in range(np.size(cross_180, 2), np.size(back_relu, 2))):
                        if(p==0):
                            if(h<=min(np.size(cross_180, 3), np.size(back_relu, 3))-1):
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,l-np.size(cross_180, 2)+1:l+1,:h+1], cross_180[:,k,:, -1-h :] ))
                            elif(h in range(np.size(cross_180, 3), np.size(back_relu, 3))):
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,l-np.size(cross_180, 2)+1:l+1, h-np.size(cross_180, 3)+1:h+1], cross_180[:,k,:,:]))
                            else:
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,l-np.size(cross_180, 2)+1:l+1, h+1 - np.size(back_relu, 3) - np.size(cross_180, 3):], cross_180[:,k,:, :np.size(cross_180, 3)+np.size(back_relu, 3)-h-1]))
                        else:
                            if(h<=min(np.size(cross_180, 3), np.size(back_relu, 3))-1):
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,:,:h+1], cross_180[:,k,-1-l : np.size(back_relu, 2)-1-l , -1-h :] ))
                            elif(h in range(np.size(cross_180, 3), np.size(back_relu, 3))):
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,:,:], cross_180[:,k,-1-l : np.size(back_relu, 2)-1-l, -1-h : np.size(back_relu, 3)-1-h]))
                            else:
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,:,h+1 - np.size(back_relu, 3) - np.size(cross_180, 3):], cross_180[:,k,-1-l : np.size(back_relu, 2)-1-l, :np.size(cross_180, 3)+np.size(back_relu, 3)-h-1]))

                    else:
                        if(p==0):
                            if(h<=min(np.size(cross_180, 3), np.size(back_relu, 3))-1):
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,l+1 - np.size(back_relu, 2) - np.size(cross_180, 2):,:h+1], cross_180[:,k,:np.size(cross_180, 2)+np.size(back_relu, 2)-l-1 , -1-h :] ))
                            elif(h in range(np.size(cross_180, 3), np.size(back_relu, 3))):
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,l+1 - np.size(back_relu, 2) - np.size(cross_180, 2):,h-np.size(cross_180, 3)+1:h+1], cross_180[:,k,:np.size(cross_180, 2)+np.size(back_relu, 2)-l-1,:]))
                            else:
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,l+1 - np.size(back_relu, 2) - np.size(cross_180, 2):,h+1 - np.size(back_relu, 3) - np.size(cross_180, 3):], cross_180[:,k, :np.size(cross_180, 2)+np.size(back_relu, 2)-l-1 , :np.size(cross_180, 3)+np.size(back_relu, 3)-h-1]))
                        else:
                            if(h<=min(np.size(cross_180, 3), np.size(back_relu, 3))-1):
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,l+1 - np.size(back_relu, 2) - np.size(cross_180, 2):,:h+1], cross_180[:,k,:np.size(cross_180, 2)+np.size(back_relu, 2)-l-1 , -1-h :] ))
                            elif(h in range(np.size(cross_180, 3), np.size(back_relu, 3))):
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,l+1 - np.size(back_relu, 2) - np.size(cross_180, 2): ,:], cross_180[:,k,:np.size(cross_180, 2)+np.size(back_relu, 2)-l-1,-1-h : np.size(back_relu, 3)-1-h]))
                            else:
                                err_input[i,k,l,h] = np.sum(np.multiply(back_relu[i,:,l+1 - np.size(back_relu, 2) - np.size(cross_180, 2):,h+1 - np.size(back_relu, 3) - np.size(cross_180, 3):], cross_180[:,k,:np.size(cross_180, 2)+np.size(back_relu, 2)-l-1, :np.size(cross_180, 3)+np.size(back_relu, 3)-h-1]))

    a.err_filter = err_filter
    err_input = err_input[:,:,1:-1,:]
    err_input = err_input[:,:,:,1:-1]
    a.err_input = err_input

    return err_input

'''this function uses the mask created in the layers.py to reproduce the matrix of the size before pooling, we multiply the 1's in the matrix to the appropriate errors. remaining elements is 0'''
def backPool(a, error, poolSize):
    tuples = list(a.indices.items())

    #err_unpool= np.zeros((np.size(matrix,0), np.size(matrix,1), np.size(matrix,2)+size-1, np.size(matrix,3)+size-1))
    err_unpool = a.mask
    for i in range(0,m):
        for l in range(0,np.size(error, 1)):
            for j in range(0,np.size(error, 2)):
                for k in range(0,np.size(error, 3)):
                    err_unpool[i,l,j:j+poolSize, k:k+poolSize] *= error[i,l,j,k]
    '''for channel in tuples:
        channel_dim = channel[0]
        for i in range(0,m):
            for j in range(0,np.size(error,2)):
                for k in range(0,np.size(error,3)):
                    #err_unpool[i, channel_dim, channel[i*imSize*imSize + j*imSize + k][0], channel[i*imSize*imSize + j*imSize + k][1]] = matrix[i,channel_dim,j,k]

                    err_unpool[i, channel_dim, channel[1][i*a.imSize*a.imSize + j*a.imSize + k][0], channel[1][i*a.imSize*a.imSize + j*a.imSize + k][1]] = error[i,channel_dim,j,k]'''
    #print(err_unpool[:1,:1,:,:])
    return err_unpool

'''normal backProp, here we call both back convolution and backpool, i tried to train the whole network for some epochs and my fcs alone for more epochs since training conv layers required much time'''

def backProp(a1,a2,a8,a9,a10,output,iter):

    #del10 = (gradient.svmGradient1(a10.final, output) + gradient.svmGradient2(a10.final, output)).transpose()
    del10 = (a10.final - output).transpose()
    del9_ = np.multiply(np.dot(a10.THETA.transpose(), del10), gradient.sigmoidGradient(a10.input.transpose()))
    del9 = del9_[1:,:]
    del8_ = np.multiply(np.dot(a9.THETA.transpose(), del9), gradient.sigmoidGradient(a9.input.transpose()))
    del8 = del8_[1:,:]
    #del7_ = np.multiply(np.dot(a8.THETA.transpose(), del8), gradient.leakyReluGradient(a8.biased.transpose()))
    #del7 = del7_[1:,:]
    #del6_ = np.multiply(np.dot(a8.THETA.transpose(), del8), gradient.sigmoidGradient(a8.biased.transpose()))
    #del6 = del6_[1:,:]
    grad_10 = (np.dot(del10, a10.input) + lamda*(np.hstack((np.zeros((np.size(a10.THETA, 0), 1)), a10.THETA[:,1:]))))/m
    grad_9 = (np.dot(del9, a9.input) + lamda*(np.hstack((np.zeros((np.size(a9.THETA, 0), 1)), a9.THETA[:,1:]))))/m
    grad_8 = (np.dot(del8, a8.input)+ lamda*(np.hstack((np.ones((np.size(a8.THETA, 0), 1)), a8.THETA[:,1:]))))/m
    #grad_7 = np.dot(del7, a7.biased)/m
    #grad_6 = np.dot(del6, a6.biased)/m


    if(iter >= 25):
        return grad_8,grad_9, grad_10
    #del5_ = np.multiply(np.dot(a6.THETA.transpose(), del6), gradient.leakyReluGradient(a6.biased.transpose()))
    #del5 = del5_[1:,:]
    #error_a5 = backPool(a5, del5.reshape((1000,10,1,1)),2)
    else:
        del2_ = np.multiply(np.dot(a8.THETA.transpose(), del8), gradient.sigmoidGradient(a8.input.transpose()))/m
        del2 = del2_[1:,:]

        error_a2 = backPool(a2, del2.reshape((m,np.size(a2.final, 1),1,1)),2)
        del1 = Backconvolution(error_a2, a2)
        #print(np.shape(del4))
        error_a1 = backPool(a1, del1, 3)

        #del2 = Backconvolution(error_a3, a3)
        #error_a2 = backPool(a2,del2,3)

        #del1 = Backconvolution(error_a2, a2)
        #error_a1 = backPool(a1,del1,3)
        del0 = Backconvolution(error_a1, a1)
    #error_a1 = backPool(a1,del1,3)
    #del0 = Backconvolution(error_a1,a1)

        return a1.err_filter,a2.err_filter,grad_8, grad_9, grad_10

init_size=8
#input = np.zeros((1000,10,10), np.float64)
input = np.zeros((m,init_size,init_size), np.float64)
output = np.zeros((m,1), np.float64)
permute = np.random.permutation(1000)
for i in permute:
    img = cv2.imread(f"E:\\Prem\\cnn\\dataset\\{i}.JPG", 0)
    input[i] = img
    output[i] = 0 if i<500 else 1
#cell1
epochs = 100

lamda = 0
lr =0.1
epsilon = 10**(-4)
filter1 = np.random.randn(2,1,3,3)*2*epsilon - epsilon
filter2 = np.random.randn(4,2,3,3)*2*epsilon - epsilon
#filter3 = np.random.randn(6,4,3,3)*2*epsilon - epsilon
#filter4 = np.random.randn(8,6,3,3)*2*epsilon - epsilon
#filter5 = np.random.randn(10,8,3,3)*2*epsilon - epsilon
#THETA6 = np.random.randn(10,11)*2*epsilon - epsilon
#THETA6 = np.random.randn(8,9)*2*epsilon - epsilon
#THETA7 = np.random.randn(10,11)*2*epsilon - epsilon
#THETA7 = np.random.randn(8,9)*2*epsilon - epsilon
#THETA8 = np.random.randn(5,11)*2*epsilon - epsilon
THETA8 = np.random.randn(4,5)*2*epsilon - epsilon
#THETA9 = np.random.randn(2,6)*2*epsilon - epsilon
THETA9 = np.random.randn(2,5)*2*epsilon - epsilon
THETA10 = np.random.randn(1,3)*2*epsilon - epsilon

cost = np.zeros((epochs))

def forwardProp(Filter1, Filter2,Theta8, Theta9, Theta10):
    a1 = layers.layer1(input.reshape((m,1,init_size,init_size)),Filter1)
    a2 = layers.layer2(a1.final,Filter2)
    #a3 = layers.layer3(a2.final,Filter3)
    #a4 = layers.layer4(a3.final,Filter4)
    #print(a4.final.shape)
    #a5 = layers.layer5(a4.final,Filter5)
    #a6 = layers.layer6(a2.final.reshape((m, init_size)), Theta6)
    #a7 = layers.layer7(a6.final, a6.resnet,Theta7)
    #a8 = layers.layer8(a6.final,Theta8)
    a8 = layers.layer8(a2.final.reshape((m, np.size(a2.final,1))),Theta8)
    a9 = layers.layer9(a8.final, Theta9)
    a10 = layers.layer10(a9.final,Theta10)
#cell2
    #loss = (costfunction.cost1(a10.final, output) + costfunction.cost2(a10.final, output))/m
    loss = (costfunction.sigmoidClassifier(a10.final, output) + 0.5*lamda*(np.sum(np.square(Theta8))+np.sum(np.square(Theta9))+np.sum(np.square(Theta10))))/m
    return loss,a1,a2,a8,a9,a10
for i in range(0, 25):
    cost[i],a1,a2,a8,a9,a10 = forwardProp(filter1,filter2,THETA8, THETA9,THETA10)
    err_filter1,err_filter2,grad_8, grad_9, grad_10 = backProp(a1,a2,a8,a9,a10,output,i)
    filter1 -= lr*err_filter1
    filter2 -= lr*err_filter2
    #filter3 -= lr*err_filter3
    #filter4 -= lr*err_filter4
    #filter5 -= lr*err_filter5
    #THETA6 -= lr*grad_6
    #THETA7 -= lr*grad_7
    THETA8 =THETA8 -  lr*grad_8

    THETA9 =THETA9 - lr*grad_9
    THETA10 =THETA10 -  lr*grad_10

for j in range(25,epochs):
    cost[j],a1,a2,a8,a9,a10 = forwardProp(filter1,filter2,THETA8,THETA9,THETA10)
    grad_8, grad_9, grad_10 = backProp(a1,a2,a8,a9,a10,output,j)
    #THETA6 -= lr*grad_6
    #THETA7 -= lr*grad_7
    THETA8 = THETA8 - lr*grad_8
    THETA9 = THETA9 -  lr*grad_9
    THETA10 =THETA10 - lr*grad_10
print(np.shape(a1.mean), np.shape(a2.mean))
weight8 = np.reshape(THETA8, (np.size(THETA8), 1))
weight9 = np.reshape(THETA9, (np.size(THETA9), 1))
weight10 = np.reshape(THETA10, (np.size(THETA10), 1))
filter_1 = filter1.reshape((np.size(filter1), 1))
filter_2 = filter2.reshape((np.size(filter2), 1))
mean_1 = a1.mean.reshape((np.size(a1.mean), 1))
std_1 = a1.std.reshape((np.size(a1.std), 1))
mean_2 = a2.mean.reshape((np.size(a2.mean), 1))
std_2 = a2.std.reshape((np.size(a2.std), 1))
with open(r'E:\Prem\cnn\weights.npy', 'w') as f:
    np.save(r'E:\Prem\cnn\weights.npy', np.vstack((weight8,weight9,weight10)))
with open(r'E:\Prem\cnn\filters.npy', 'w') as f:
    np.save(r'E:\Prem\cnn\filters.npy', np.vstack((filter_1, filter_2)))
with open(r'E:\Prem\cnn\norm.npy', 'w') as f:
    np.save(r'E:\Prem\cnn\norm.npy', np.vstack((mean_1, std_1, mean_2, std_2)))
plt.plot([k for k in range(0,epochs)], cost)
plt.show()
accuracy = np.sum(np.fabs(output-a10.final))/m
print(accuracy)
print(cost)
#print(arr[1,a5.indices[0][10][0], a5.indices[0][10][1]])
#backProp(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,output)
