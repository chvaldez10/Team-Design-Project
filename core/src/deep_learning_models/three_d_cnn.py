import torch.nn as nn
import torch.nn.functional as F

class Basic3DCNN(nn.Module):
    def __init__(self):
        super(Basic3DCNN, self).__init__()
        self.conv1 = nn.Conv3d(in_channels=3, out_channels=16, kernel_size=(3, 3, 3), stride=1, padding=1)
        self.pool = nn.MaxPool3d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv3d(16, 32, kernel_size=(3, 3, 3), stride=1, padding=1)
        # Updated size based on your input dimensions after flattening
        self.fc1 = nn.Linear(2508800, 512)   # Adjusted to calculated size - 32 * 56* 56 * 24
        self.fc2 = nn.Linear(512, 2)  # Assuming 2 classes

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        # Adjust the flattening operation to match the updated fc1 input size
        x = x.view(-1, 2508800)  # Flatten the tensor for the fully connected layer
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x