import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from datetime import datetime
import activations
import layers
import train





df = pd.read_excel(r'E:\Prem\python\spyder\data.xlsx')
df_ = df
cont = list(df["continent"].unique())
cont.remove(cont[-1])
loc = list(df["location"].unique())
loc.remove('World')
loc.remove('International')
df = df.dropna(subset = ['continent', 'new_cases', 'new_deaths'])
copy = df
#'''to preserve the original dataframe'''
for continent in cont:
    df.loc[df.continent == continent, "continent"] = float(cont.index(continent) + 1)    #'''Asia=1, etc'''
for location in loc:
    df.loc[df.location == location, "location"] = float(loc.index(location) + 1)
    arr=(df.loc[df.location == loc.index(location) + 1, ["date", "new_cases", "new_deaths", "continent", "location"]]).to_numpy()
    arr1 = arr[:,:3]
    arr1[1:,1:3]=arr[:-1,1:3]
                                                  #''' the date of nth row in a location shld match with new cases and death of n-1th location'''
    arr1 = arr1[1:,:]
    rows, columns = np.indices((np.size(arr1,0),1))
    arr1[rows, columns] = rows + 2
    arr1 = np.insert(arr1, 1, arr1[:,0]**2, axis=1)      # ''' i plotted new cases and deaths against number of days and found it to be a quadrtatic dependence'''
    if(loc.index(location) == 0):
        previous = arr1                                          #'''parsing location by location and preparing the input for layer 2'''
        #previous_train = arr1[:math.floor(0.8 * np.size(arr1,0)), :]
        #previous_test = arr1[math.floor(0.8 * np.size(arr1,0)):,:]

        Y=arr[1:,1:3]                                             #'''parsing location by location and preparing the output layer. '''
        #Y_train = arr[1:math.floor(0.8 * np.size(arr1,0))+1, 1:3]
        #Y_test = arr[math.floor(0.8 * np.size(arr1,0))+1:, 1:3]

        D=arr[1:,3:]                                               #'''parsing location by location and preparing the input for layer 1'''

        #D_train = arr[1:math.floor(0.8 * np.size(arr1,0))+1, 3:]
        #D_test = arr[math.floor(0.8 * np.size(arr1,0))+1:, 3:]

    else:
        #previous_train = np.vstack((previous_train, arr1[:math.floor(0.8 * np.size(arr1,0)), :]))
        #previous_test = np.vstack((previous_test, arr1[math.floor(0.8 * np.size(arr1,0)):,:]))
        previous = np.vstack((previous, arr1))    # second layer input

        #Y_train = np.vstack((Y_train, arr[1:math.floor(0.8 * np.size(arr1,0))+1, 1:3] ))
        #Y_test = np.vstack((Y_test, arr[math.floor(0.8 * np.size(arr1,0))+1:, 1:3]))
        Y = np.vstack((Y,arr[1:,1:3]))

        #D_train = np.vstack((D_train, arr[1:math.floor(0.8 * np.size(arr1,0))+1, 3:] ))
        #D_test = np.vstack((D_test, arr[math.floor(0.8 * np.size(arr1,0))+1:, 3:]))
        D = np.vstack((D,arr[1:,3:]))                                                 #''' first row of each location should be omitted because it doesnt have previous cases and deaths'''
#O = np.ones((np.size(D,0), 1))
epsilon = 10**(-10)
Theta1 = (np.random.rand(5,3)) * (2*epsilon) - epsilon   #''' 5x3 matrix whose absolute values are less than epsilon'''
Theta2 = (np.random.rand(7,10)) * (2*epsilon) - epsilon
Theta3 = (np.random.rand(5,8)) * (2*epsilon) - epsilon
Theta4 = (np.random.rand(2,6)) * (2*epsilon) - epsilon               #''' random initialization of weights'''
np.set_printoptions(threshold=np.inf)
D_Normed = layers.layer1(D)

#D_Normed, meanD, stdD = featureNormalize.fNorm(D_train)
#D_Normed_test, meanDtest, stdDtest = featureNormalize.fNorm(D_test)

previous_Normed, meanPre, stdPre = train.fNorm(previous)
#previous_Normed, meanPre, stdPre = featureNormalize.fNorm(previous_train)
#previous_Normed_test, meanPretest, stdPretest = featureNormalize.fNorm(previous_test)

Y_Normed=layers.layer5(Y)      #since input to second layer is normed lets norm this also
#Y_Normed, meanY, stdY = featureNormalize.fNorm(Y_train)
#Y_Normed_test, meanYtest, stdYtest = featureNormalize.fNorm(Y_test)
num_iters = 400.0
#Lambda = [0, 0.02 ** x for x in range(1,11)]
Lambda=0
lr = 0.1
J_hist = np.arange(num_iters)                                # ''' to plot it against num of iterations'''
#J_test_hist = []
#hypo_hist = np.zeros((27150, 2, int(num_iters)))
hypo_hist = np.zeros((np.size(Y_Normed.z, 0), 2, int(num_iters)))



#for Lambda_ in Lambda:   '''to check which lambda gives the smallest error'''

    #Theta1 = (np.random.rand(5,3)) * (2*epsilon) - epsilon
    #Theta2 = (np.random.rand(7,10)) * (2*epsilon) - epsilon
    #Theta3 = (np.random.rand(5,8)) * (2*epsilon) - epsilon
    #Theta4 = (np.random.rand(2,6)) * (2*epsilon) - epsilon      '''re initialize theta for every lambda_

for i in range(0,int(num_iters)):           # '''gradient descent'''
    #hypo_hist[:,:,i], J_hist[i], des1, des2, des3, des4, meanz1, stdz1, meanz2, stdz2, meanz3, stdz3  = hypothesis.hypothesis(matrix_lay1, previous_Normed, Y_Normed, Theta1, Theta2, Theta3, Theta4, num_iters, Lambda)
    hypo_hist[:,:,i], J_hist[i], des1, des2, des3, des4, meanz1, stdz1, meanz2, stdz2, meanz3, stdz3  = train.forBackprop(D_Normed.z, previous_Normed, Y_Normed.z, Theta1, Theta2, Theta3, Theta4, Lambda)
    Theta1[:,1:] = Theta1[:,1:] - lr*des1
    Theta2[:,1:] = Theta2[:,1:] - lr*des2
    Theta3[:,1:] = Theta3[:,1:] - lr*des3
    Theta4[:,1:] = Theta4[:,1:] - lr*des4

#J_test_hist.append(hypothesis.costTest(np.hstack((O[:np.size(D_Normed_test, 0), :], D_Normed_test)), previous_Normed_test, Y_Normed_test, Theta1, Theta2, Theta3, Theta4))

weight1 = Theta1.reshape((np.size(Theta1), 1))
weight2 = Theta2.reshape((np.size(Theta2), 1))
weight3 = Theta3.reshape((np.size(Theta3), 1))
weight4 = Theta4.reshape((np.size(Theta4), 1))
with open(r'E:\Prem\python\spyder\weights.npy', 'w') as f:
    np.save(r'E:\Prem\python\spyder\weights.npy', np.vstack((weight1, weight2, weight3, weight4)))
with open(r'E:\Prem\python\spyder\norm.npy', 'w') as f:
    np.save(r'E:\Prem\python\spyder\norm.npy', np.hstack((D_Normed.mean, D_Normed.std, meanPre, stdPre, meanz1, stdz1, meanz2, stdz2, meanz3, stdz3, Y_Normed.mean, Y_Normed.std)))

#print(J_test_hist)
#plt.plot(list(range(0, len(Lambda) )), J_test_hist)
#plt.title(lr)
#plt.show()
print((np.multiply(hypo_hist[:,:,-1], Y_Normed.std) + Y_Normed.mean ))
print(Y_Normed.mean, Y_Normed.std)
print(hypo_hist[:20,:,-1])
#dataframe = pd.DataFrame(np.hstack((Y, (np.multiply(hypo_hist[:,:,-1], stdY) + meanY ))))
#writer = pd.ExcelWriter(r'E:\Prem\python\spyder\train0.xlsx', engine='xlsxwriter')
#dataframe.to_excel(writer)
#writer.save()

plt.plot(list(range(1, int(num_iters) + 1)), list(J_hist))
plt.title(lr)
plt.show()
print(Theta1, Theta2, Theta3, Theta4)


'''Theta1 = np.array([[ 6.17193929e-09, -4.21474496e-07, 3.66628700e-07],
[-9.65991963e-09, 2.93354542e-06, -3.89241153e-06],
[-4.10761245e-09, 6.40786286e-07, -1.69388560e-07],
[ 7.84370268e-09, -5.57140316e-07, -3.15166975e-07],
[-9.96094587e-09, -2.92220263e-06, 2.73994030e-06]])

Theta2 = np.array([[ 4.17290708e-09, -9.25830186e-05, -1.01920487e-04, -9.22016450e-05,
 -2.22913583e-05, -1.67088235e-04, -1.20741738e-04, -9.46335752e-06,
  1.45191981e-02, -3.60643935e-03],
[-3.85601950e-09, 3.40840144e-05, 1.48962721e-04, 1.76475969e-04,
  6.55802175e-05, 2.70827466e-04, -4.83797117e-05, 5.83685248e-05,
  1.36895679e-02, -1.11765660e-03],
[-3.93535712e-09 , 2.23133930e-05 , 1.55808082e-07, -1.29255037e-05,
 -9.65113353e-06 , 5.18438759e-06 , 7.31596336e-05 , 3.62972679e-05,
  8.15625044e-03 , 1.29051932e-02],
[-6.54038048e-09, -9.14464155e-05, -5.12924400e-05, -2.71586711e-05,
 -3.60766314e-05 , 1.05591429e-04 ,-1.00140030e-04 , 1.98272289e-04,
  9.15942215e-04 ,-2.42193687e-02],
[-4.39558726e-10 , 3.76799778e-05 , 3.38915214e-05,  3.51056727e-05,
  3.59316733e-05, -5.25108379e-05 ,-2.25123929e-05, -1.26511133e-04,
 -1.36637320e-02, -4.58978466e-03],
[ 4.71341558e-10 ,-8.94587627e-05, -3.41160508e-05, -1.52966874e-05,
 -4.80730524e-05,  1.14079509e-04, -7.53175549e-05,  1.64530411e-05,
 -4.36947875e-03, -1.47294809e-02],
[ 3.69687756e-09, -4.69188575e-05, -4.64400966e-05, -6.09107369e-05,
 -8.49120110e-05,  5.32160371e-05 , 8.61511083e-05, -2.25645012e-04,
  2.88430569e-03 , 2.60283682e-02]])

Theta3 = np.array([[-7.90757789e-09, -9.48047750e-02 ,-8.07670010e-02, -1.23058134e-02,
-5.36945853e-02,  6.00474827e-02, -1.17375011e-02,  3.46539138e-02],
[-7.87007562e-09,  2.07871998e-02 , 7.17840922e-03, -6.26141596e-02,
1.13137179e-01 , 2.29668498e-02 , 7.26184040e-02, -1.16599342e-01],
[ 8.39518337e-11,  5.92827427e-02 , 5.40639966e-02 , 2.79914685e-02,
5.43478498e-03, -5.01108978e-02, -1.38248778e-02,  8.78481637e-03],
[ 3.10031991e-09, -3.47345259e-02, -3.45823183e-02, -3.30121394e-02,
2.17732502e-02,  3.89310891e-02 , 2.60263708e-02, -3.13296172e-02],
[-5.21820482e-10,  3.78360271e-02,  2.38654925e-02, -3.98149806e-02,
8.87306798e-02,  1.59127094e-03,  5.23848300e-02 ,-8.49800080e-02]])

Theta4 = np.array([[-2.08924376e-09, -4.25575221e-01, -1.22636198e-01,  2.99709873e-01,
-2.27054247e-01, -1.06133192e-03],
[-5.13135864e-09,  1.25697833e-01, -4.40681662e-01 , 8.02053984e-02,
-1.75069309e-01 ,-3.91259411e-01]]
)

meanz1 = np.array([7.059663760587769e-10, -9.682197705264972e-09, -8.685301355409861e-09,
 2.359130711628766e-09, 9.519730098542839e-09, -3.428514816351247e-17,
 6.231143033332437e-17, 2.937158366764105e-15, -4.1404041541421706e-15])

stdz1 = np.array([2.9400910e-08, 2.4580363e-08, 3.4485474e-08, 8.1828311e-10, 1.7825647e-09,
 1.0000156e+00, 1.0000041e+00, 9.9990112e-01, 9.9995160e-01])

meanz2 = np.array([-9.08411158678766e-09, -4.489058346320806e-09, -8.95301723300529e-09,
 -5.8924174561534196e-09, -8.57200902540911e-10, 1.0897506957749044e-09,
 -9.853791662740609e-09])

stdz2 = np.array([0.01738858 ,0.01469407 ,0.01144189 ,0.02465651, 0.01934653 ,0.01590947,
 0.00863869])

meanz3 = np.array([-1.2787779633319691e-09 ,4.839446247345136e-09 ,5.666050836753389e-09,
 3.022212606143042e-09, 7.273584050823821e-09])

stdz3 = np.array([[0.24553615, 0.2628407,  0.31469563, 0.18597071, 0.20817026]])'''

cont_input = input(str("enter the continent"))
cont_input_float = float(cont.index(cont_input) + 1)
loc_input = input(str("enter the country"))
loc_input_float = float(loc.index(loc_input) + 1)
row = (df.loc[df.location == loc_input_float, ["date", "new_cases", "new_deaths"]]).to_numpy()

day_input = input(str("enter the date"))
date_format = "%d-%m-%Y"
a = datetime.strptime(day_input, date_format)

delta = a - row[-1,0]



days_needed = np.arange(np.size(row, 0) + 2, np.size(row,0) + 2 + delta.days, dtype=np.float32)

A = np.array([cont_input_float, loc_input_float], dtype=np.float32)

A = np.divide(A - D_Normed.mean, D_Normed.std)
A = np.insert(A,0,1,axis=0)

prev_case = row[-1,1]
prev_deaths = row[-1,2]
print(prev_case, prev_deaths)
prev_case = (prev_case-Y_Normed.mean[0])/Y_Normed.std[0]
prev_deaths = (prev_deaths-Y_Normed.mean[1])/Y_Normed.std[1]
print(prev_case, prev_deaths)

for i in days_needed:
    #calc1=np.dot(A, Theta1.transpose())
    calc1 = activations.activation(A, Theta1)

    calc1_ = np.hstack((calc1, np.array([i, i**2, prev_case, prev_deaths]) ))

    calc1Normed = np.divide(calc1_ - meanz1 , stdz1)

    calc1_Normed = np.insert(calc1Normed,0,1,axis=0)

    calc2 = activations.activation(calc1_Normed, Theta2)
    calc2Normed = np.divide(calc2 - meanz2, stdz2)
    calc2_Normed = np.insert(calc2Normed,0,1,axis=0)

    calc3 = activations.activation(calc2_Normed, Theta3)
    calc3Normed = np.divide(calc3 - meanz3, stdz3)
    calc3_Normed = np.insert(calc3Normed,0,1,axis=0)

    calc4 = activations.activation(calc3_Normed, Theta4)
    print(calc4)
    prev_case, prev_deaths = calc4
    print(prev_case, prev_deaths)                                                 #''' we shld give normalized input again if we unnormalize here. so we can leave it as it is'''
print("the predicated new cases and deaths is ", prev_case, prev_deaths)
print(np.multiply(np.floor(np.fabs(calc4.astype(np.float64), dtype=np.float64)), Y_Normed.std) + Y_Normed.mean) #unnorming
