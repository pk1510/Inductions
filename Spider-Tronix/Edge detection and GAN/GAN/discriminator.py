import torch
import torch.nn as nn


class Discriminator(nn.Module):
    def __init__(self, channels_img, features_d, gpus):
        super(Discriminator, self).__init__()
        self.gpus = gpus
        self.net = nn.Sequential(
            # N x channels_img x 64 x 64
            nn.Conv2d(channels_img, features_d, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2),
            # N x features_d x 32 x 32
            nn.Conv2d(features_d, features_d * 2, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(features_d * 2),
            nn.LeakyReLU(0.2),
            nn.Conv2d(
                features_d * 2, features_d * 4, kernel_size=4, stride=2, padding=1
            ),
            nn.BatchNorm2d(features_d * 4),
            nn.LeakyReLU(0.2),
            nn.Conv2d(
                features_d * 4, features_d * 8, kernel_size=4, stride=2, padding=1
            ),
            nn.BatchNorm2d(features_d * 8),
            nn.LeakyReLU(0.2),
            # N x features_d*8 x 4 x 4
            nn.Conv2d(features_d * 8, 1, kernel_size=4, stride=2, padding=0),
            # N x 1 x 1 x 1
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.net(x)
