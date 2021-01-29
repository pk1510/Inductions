import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from forProp import model

workers = 0
lr = 0.006
num_epochs = 30
beta1 = 0.5
m = 1250
img_size = 256
channels_img = 3
daisy = torch.zeros(250,1)
dandelion = torch.ones(250,1)
rose = torch.ones(250,1)*2
sunflower = torch.ones(250,1)*3
tulip = torch.ones(250,1)*4
label = torch.cat((daisy, dandelion, rose, sunflower, tulip), 0).long()

rootDir = r"E:\Prem\rmi\AI\flowers"

def weights_initialize(m):
    classname = m.__class__.__name__
    if(classname.find('Conv') != -1):
        nn.init.normal_(m.weight.data, 0.0, 1.0)
    elif classname.find('BatchNorm') != -1:
        nn.init.normal_(m.weight.data, 0.0, 1.0)
        nn.init.constant_(m.bias.data, 0)

my_transforms = transforms.Compose(
    [
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        transforms.Normalize((127.5,127.5,127.5), (127.5,127.5,127.5))
    ]
)
dataset = datasets.ImageFolder(root=rootDir, transform=my_transforms)
dataloader = DataLoader(dataset, batch_size=m, shuffle=False, num_workers = workers)
device = torch.device("cpu")
Model = model(channels_img, img_size)
Model.apply(weights_initialize)
optimizer = optim.Adam(Model.parameters(), lr=lr, betas=(beta1, 0.999))
Model.train()
criterion = nn.CrossEntropyLoss()
print("training...")

for epoch in range(num_epochs):
    for batch_idx, (data, targets) in enumerate(dataloader):
        data = data.to(device)
        batch_size = data.shape[0]

        ### Train Discriminator: max log(D(x)) + log(1 - D(G(z)))
        Model.zero_grad()
        #real_cpu = data.to(device)
        #label = (torch.ones(config.batch_size) * 0.9).to(device)
        output = Model(data)
        loss = criterion(output, label[:,0])
        final = output.mean().item()
        loss.backward()
        optimizer.step()
        print(
                f"Epoch [{epoch}/{num_epochs}] Batch {batch_idx}/{len(dataloader)} \
                  Loss : {loss:.4f} out: {final:.4f}"
            )
torch.save(Model.state_dict(), "./models.pt")
