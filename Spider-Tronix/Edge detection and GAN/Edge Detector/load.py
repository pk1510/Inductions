import cv2
import numpy as np

dataset = (np.ones((1000,8,8), np.uint8))*255
for i in range(0,250):                                           #veritcal edges with right half as white
    col_number = np.random.randint(1,6)
    dataset[i,:,:col_number] = np.random.randint(0,128,size=(1,8,col_number))
    cv2.imwrite(f"E:\\Prem\\cnn\\dataset\\{i}.JPG", dataset[i,:,:])
for i in range(250,500):
    col_number = np.random.randint(1,6)
    dataset[i,:,col_number:] = np.random.randint(0,128,size=(1,8,8-col_number))
    cv2.imwrite(f"E:\\Prem\\cnn\\dataset\\{i}.JPG", dataset[i,:,:])
for i in range(500,750):
    row_number = np.random.randint(1,6)
    dataset[i,:row_number,:] = np.random.randint(0,128,size=(1,row_number,8))
    cv2.imwrite(f"E:\\Prem\\cnn\\dataset\\{i}.JPG", dataset[i,:,:])
for i in range(750,1000):
    row_number = np.random.randint(1,6)
    dataset[i,row_number:,:] = np.random.randint(0,128,size=(1,8-row_number,8))
    cv2.imwrite(f"E:\\Prem\\cnn\\dataset\\{i}.JPG", dataset[i,:,:])
print(dataset[2].shape)
