import torch
import torch.nn as nn

class model(nn.Module):
    def __init__(self, channels_img, img_size):
        super(model, self).__init__()
        self.net = nn.Sequential(
        #Nxchannels_imgx64x64
            nn.Conv2d(channels_img, channels_img*2, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.02),
            nn.MaxPool2d(kernel_size=2, stride=2),
        #Nxchannels_img*2x16x16
            nn.Conv2d(channels_img*2, channels_img*3, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(channels_img*3),
            nn.LeakyReLU(0.02),
            nn.MaxPool2d(kernel_size=2, stride=2),
        #Nxchannels_img*3x16x16
            nn.Conv2d(channels_img*3, channels_img*4, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(channels_img*4),
            nn.LeakyReLU(0.02),
            nn.MaxPool2d(kernel_size=2, stride=2),
        #Nxchannels_img*4x4x4
            nn.Conv2d(channels_img*4, 1, kernel_size=1, stride=1, padding=0),
            nn.Flatten(start_dim = 1, end_dim = 3),
        #Nx1x4x4
            nn.Linear(16,8),
            nn.Sigmoid(),
            nn.Linear(8,5),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)
