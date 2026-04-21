# Setup
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
from torchsummary import summary
from PIL import Image

class Net(nn.Module):
    """
    3-layer CNN network with max pooling

    Args:
        in_channels: number of features of the input image ("depth of image")
        hidden_channels: number of hidden features ("depth of convolved images")
        out_features: number of features in output layer
    """

    def __init__(self, in_channels, hidden_channels, out_features):
        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(in_channels, hidden_channels[0],
                               kernel_size=3,
                               padding=1)
        self.relu1 = nn.ReLU()
        self.max_pool1 = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(hidden_channels[0], hidden_channels[1],
                               kernel_size=5,
                               padding=2)
        self.relu2 = nn.ReLU()
        self.max_pool2 = nn.MaxPool2d(2)
        
        self.fc = nn.Linear(56*56*hidden_channels[1], out_features)

    def forward(self, x):
        # First convolutional layer
        x = self.conv1(x)
        # Activation function
        x = self.relu1(x)
        # Max pool
        x = self.max_pool1(x)
        # Second convolutional layer
        x = self.conv2(x)
        # Activation function
        x = self.relu2(x)
        # Max pool
        x = self.max_pool2(x)
        # Flatten
        x = x.view(x.size(0), -1)
        # Fully connected layer
        x = self.fc(x)
        return x
    
    

# Preprocessing data: convert to tensors and normalize by subtracting dataset
# mean and dividing by std.

datadir = r"C:\Users\Student\Desktop\MmM\Code\Microscope_Control\Mitosis Detection\DL\data-mitosis"

transform = transforms.Compose([transforms.Resize((512,512)),
                                transforms.Grayscale(num_output_channels=1),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.5],
                                                     std=[0.5])])

train_data = datasets.ImageFolder(root= datadir + r'/train', transform=transform)
test_data = datasets.ImageFolder(root= datadir + r'/val', transform=transform)



# Define data loaders used to iterate through dataset
train_loader = DataLoader(train_data, batch_size=16, shuffle=True)
test_loader = DataLoader(test_data, batch_size=16)

def try_gpu():
    """
    If GPU is available, return torch.device as cuda:0; else return torch.device
    as cpu.
    """
    if torch.cuda.is_available():
        device = torch.device('cuda:0')
    else:
        device = torch.device('cpu')
    return device

def evaluate_accuracy(data_loader, net, device=torch.device('cpu')):
    """Evaluate accuracy of a model on the given data set."""
    net.eval()  #make sure network is in evaluation mode

    #init
    acc_sum = torch.tensor([0], dtype=torch.float32, device=device)
    n = 0

    for X, y in data_loader:
        # Copy the data to device.
        X, y = X.to(device), y.to(device)
        with torch.no_grad():
            y = y.long()
            acc_sum += torch.sum((torch.argmax(net(X), dim=1) == y))
            n += y.shape[0] #increases with the number of samples in the batch
    return acc_sum.item()/n

# Define the channel sizes and output dim
in_channels = 1
hidden_channels = [5, 6]
out_features = 2


# Training parameters
learning_rate = 0.001
epochs = 3



net = Net(in_channels, hidden_channels, out_features)
optimizer = torch.optim.SGD(net.parameters(), lr = learning_rate)

criterion = nn.CrossEntropyLoss()
summary(net, (in_channels, 224, 224), device='cpu') # (in_channels, height, width)

# Define list to store losses and performances of each iteration
train_losses = []
train_accs = []
test_accs = []

# Try using gpu instead of cpu
device = try_gpu()
#punishing attempt
weights = torch.tensor([2.0, 1.0], device=device)
criterion = nn.CrossEntropyLoss(weight=weights)

for epoch in range(epochs):

    # Network in training mode and to device
    net.train()
    net.to(device)

    # Training loop
    for i, (x_batch, y_batch) in enumerate(train_loader):

        # Set to same device
        x_batch, y_batch = x_batch.to(device), y_batch.to(device)

        # Set the gradients to zero
        optimizer.zero_grad()

        # Perform forward pass
        y_pred = net(x_batch)

        # Compute the loss
        loss = criterion(y_pred, y_batch)
        train_losses.append(loss.item())

        # Backward computation and update
        loss.backward()
        optimizer.step()

    # Compute train and test error
    train_acc = 100*evaluate_accuracy(train_loader, net.to('cpu'))
    test_acc = 100*evaluate_accuracy(test_loader, net.to('cpu'))

    # Development of performance
    train_accs.append(train_acc)
    test_accs.append(test_acc)

    # Print performance
    print('Epoch: {:.0f}'.format(epoch+1))
    print('Accuracy of train set: {:.00f}%'.format(train_acc))
    print('Accuracy of test set: {:.00f}%'.format(test_acc))
    print('')


# Plot training curves
plt.figure(figsize=(9,4))
plt.subplot(1,2,1)
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.plot(train_losses)
plt.grid()
plt.show()

plt.subplot(1,2,2)
plt.xlabel('Epochs')
plt.ylabel('Accuracy (%)')
plt.plot(train_accs, label = 'train')
plt.plot(test_accs, label = 'test')
plt.legend()
plt.grid()
plt.show()