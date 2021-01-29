import numpy as np

with open(r'E:\Prem\python\spyder\weights.npy', 'r') as f:
    weights = np.load(r'E:\Prem\python\spyder\weights.npy',allow_pickle=True)
Theta1 = weights[:15,0].reshape((5,3))
Theta2 = weights[15:85,0].reshape((7,10))
Theta3 = weights[85:125,0].reshape((5,8))
Theta4 = weights[125:,0].reshape((2,6))

with open(r'E:\Prem\python\spyder\norm.npy', 'r') as f:
    norms = np.load(r'E:\Prem\python\spyder\norm.npy',allow_pickle=True)
meanD = norms[:2]
stdD = norms[2:4]
meanPre = norms[4:8]
stdPre = norms[8:12]
meanz1 = norms[12:21]
stdz1 = norms[21:30]
meanz2 = norms[30:37]
stdz2 = norms[37:44]
meanz3 = norms[44:49]
stdz3 = norms[49:54]
meanY = norms[54:56]
stdY = norms[56:58]
print(np.size(weights), np.size(norms))
