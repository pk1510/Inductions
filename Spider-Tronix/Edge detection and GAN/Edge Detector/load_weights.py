import numpy as np

with open(r'E:\Prem\cnn\weights.npy', 'r') as f:
    weights = np.load(r'E:\Prem\cnn\weights.npy',allow_pickle=True)
THETA8 = weights[:20, 1].reshape((4,5))
THETA9 = weights[20:30].reshape((2,5))
THETA10 = weights[30:].reshape((1,3))

with open(r'E:\Prem\cnn\filters.npy', 'r') as f:
    filters = np.load(r'E:\Prem\cnn\filters.npy',allow_pickle=True )
filter1 = filters[:18].reshape((2,1,3,3))
filter2 = filters[18:].reshape((4,2,3,3))
with open(r'E:\Prem\cnn\norm.npy', 'r') as f:
    norm = np.load(r'E:\Prem\cnn\norm.npy',allow_pickle=True)
mean_1 = norm[]
