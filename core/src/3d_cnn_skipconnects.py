# -*- coding: utf-8 -*-
"""3D-CNN-EditedMar28.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N4Jl-4S57KTTi3FZfvkGCnh6F2CfKyXj

## Import Libraries
"""

import re
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, datasets
from sklearn.metrics import confusion_matrix, roc_curve, auc
import os
from typing import List, Tuple
from itertools import product
from PIL import Image
import wandb
import random
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import time

# WandB Information
wandb.login(key='fbe9062d8afc2237e9c82b76146a6be8f5683c2f')
wandb.init(project='3D-CNN', entity='detecting-respiratory-pattern')

# Define Checkpoint Information
model_save_dir = './model_checkpoints'
current_time = datetime.now().strftime('%Y%m%d-%H%M%S')
model_filename = f'best_model_{current_time}.pth'
model_save_path = os.path.join(model_save_dir, model_filename)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
"""## Load Dataset

Number of Frames used per video

- 100 frames are used from each sample. For samples with less than 100, padding is applied. This number was chosen as a balance between using a lot of data but not using too much padding since that can bring about inaccuracies.
"""

# Define Number of frames used for each sample.
max_frames = 100
BLANKET_STATUS = ["With Blankets", "Without Blankets"]
DISTANCE_MEASURES = ["2 Meters", "3 Meters"]
BREATHING_LABELS = ["Hold Breath", "Relaxed"]

def extract_number(filename: str) -> int:
    match = re.search(r"(\d+)\.pt$", filename)
    if match:
        return int(match.group(1))
    return None

class BreathingDataset(Dataset):
    def __init__(self, root_dir, blanket_condition=None, distance=None, transform=None, max_frames=max_frames):
        """
        Initialize the dataset.

        :param root_dir: Base directory for the dataset (e.g., path to 'Training').
        :param blanket_condition: 'With Blankets' or 'Without Blankets', use None to include both.
        :param distance: '2 Meters' or '3 Meters', use None to include both distances.
        :param transform: Transformations to be applied to each image.
        :param max_frames: Maximum number of frames to use from each video sequence.
        """
        self.root_dir = root_dir
        self.blanket_condition = blanket_condition
        self.distance = distance
        self.transform = transform
        self.max_frames = max_frames
        self.samples: List[Tuple[List[str], int]] = []
        self._generate_samples()

    def _generate_samples(self) -> None:
        """
        Generates samples by iterating over all combinations of conditions, distances, and labels.
        """
        conditions = [self.blanket_condition] if self.blanket_condition else BLANKET_STATUS
        distances = [self.distance] if self.distance else DISTANCE_MEASURES

        for condition, distance, label in product(conditions, distances, BREATHING_LABELS):
            self._add_samples_for_condition_distance_label(condition, distance, label)

    def _add_samples_for_condition_distance_label(self, condition: str, distance: str, label: str) -> None:
        """
        Adds image samples for a given condition, distance, and label.
        """
        label_path = os.path.join(self.root_dir, condition, distance, label)
        for subject_path in filter(lambda p: os.path.isdir(os.path.join(label_path, p)), os.listdir(label_path)):
            subject_full_path = os.path.join(label_path, subject_path)
            images = self._get_sorted_images(subject_full_path)
            if images:
                self.samples.append((images, 0 if label == "Hold Breath" else 1))

    def _get_sorted_images(self, subject_path: str) -> List[str]:
        """Retrieves and sorts .pt files in a subject's directory."""
        frames_path = os.listdir(subject_path)
        images = [os.path.join(subject_path, img) for img in frames_path if img.endswith(".pt")]
        images = sorted(images, key=extract_number)
        return images


    def __len__(self) -> int:
        """Returns the total number of samples."""
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        """Retrieves a sample and its label, applying transformations as needed."""
        images_path, label = self.samples[idx]
        images = [self._load_image(img_path) for img_path in images_path]

        if len(images) > self.max_frames:
            # Calculate the range for possible start indices
            max_start_index = len(images) - self.max_frames
            start_index = random.randint(0, max_start_index)
            images = images[start_index:start_index + self.max_frames]

        elif len(images) < self.max_frames:
            # If there are fewer than max_frames, pad with zeros
            padding = [torch.zeros_like(images[0]) for _ in range(self.max_frames - len(images))]
            images.extend(padding)

        # if random.random() > 0.5:
        #     images = [self._horizontal_flip(img) for img in images]

        return torch.stack(images), label

    def _load_image(self, img_path: str) -> torch.Tensor:
        """Loads a pre-transformed image tensor directly from a .pt file."""
        return torch.load(img_path)


    def _horizontal_flip(self, img: torch.Tensor) -> torch.Tensor:
        """Applies horizontal flip to an image."""
        return torch.flip(img, dims=[2])

"""## Data Preprocessing
- Resize image that is suitable for CNN architecture and that can be suported by computation power avaliable
    - common pixel dimension 224 by 224 & 112 by 112
    - however want to maintain dimensions (1920 by 1080) to  (320, 180)  (width, height)
- Crop images based on coordinates to only process region of interest
    - Coordinates determined using average of coordinates over all frames per video
    - crop_coordinates = [700.4810791015625, 300, 1766.735595703125, 1080.0]
    - CNN translation invariant so cropping wouldn't change anything excpet data loss as legs cut out in some areas
    - cropping could help with reducing computation as less pixels compute ?
"""

# preprocess images
# transform = transforms.Compose([
#     transforms.Resize((180, 320)),
#     transforms.ToTensor(),
# ])

# Specify which conditions / configurations to include
# WITHOUT BLANKETS and 2m and 3m (distance = none)

train_dataset_without_blankets = BreathingDataset('/work/TALC/enel645_2024w/design_project_yene/270_480_all_transform_10-fps/Train', blanket_condition='Without Blankets', distance=None)
val_dataset_without_blankets = BreathingDataset('/work/TALC/enel645_2024w/design_project_yene/270_480_all_transform_10-fps/Validation', blanket_condition='Without Blankets', distance=None)
test_dataset_without_blankets = BreathingDataset('/work/TALC/enel645_2024w/design_project_yene/270_480_all_transform_10-fps/Test', blanket_condition='Without Blankets', distance=None)

train_loader = DataLoader(train_dataset_without_blankets, batch_size=2, shuffle=True)  # Shuffle for training - this shuffles the samples (i.e. sets of frames, rather than individual frames.)
val_loader = DataLoader(val_dataset_without_blankets, batch_size=2, shuffle=False)  # No shuffle for validation
test_loader = DataLoader(test_dataset_without_blankets, batch_size=2, shuffle=False)  # No shuffle for testing

def imshow(img):
    img = np.transpose(img, (1, 2, 0)) # matplotlib only takes height width channels (initially it is channels, height, width)
    plt.imshow(img)
    plt.show()

# Get a batch of training data
images, labels = next(iter(train_loader))

# Randomly select a sample index
sample_index = random.randint(0, len(images) - 1)

# Randomly select 5 frame indices
frame_indices = random.sample(range(images.size(1)), 5)

# Show the selected frames
for idx in frame_indices:
    single_image = images[sample_index, idx]
    imshow(single_image)
    print('Label:', 'Hold Breath' if labels[sample_index] == 1 else 'Relaxed')

"""Define 3D CNN Model that follows VGG architecture
- consists of alternating convolution layers followed by max pooling layers
- then a dropout layer and dense layer to classify videos
"""

class Basic3DCNN(nn.Module):
    def __init__(self):
        super(Basic3DCNN, self).__init__()
        # Convolutional layers
        self.conv1 = nn.Conv3d(in_channels=3, out_channels=30, kernel_size=(3, 3, 3), padding=1)
        self.conv2 = nn.Conv3d(30, 30, kernel_size=(3, 3, 3), padding=1)
        self.conv3 = nn.Conv3d(in_channels=30, out_channels=60, kernel_size=(3, 3, 3), padding=1)
        self.conv4 = nn.Conv3d(60, 60, kernel_size=(3, 3, 3), padding=1)
        self.conv5 = nn.Conv3d(in_channels=60, out_channels=120, kernel_size=(3, 3, 3), padding=1)
        self.conv6 = nn.Conv3d(120, 120, kernel_size=(3, 3, 3), padding=1)
        self.conv7 = nn.Conv3d(in_channels=120, out_channels=240, kernel_size=(3, 3, 3), padding=1)
        self.conv8 = nn.Conv3d(240, 240, kernel_size=(3, 3, 3), padding=1)
        
        # Pooling layer
        self.pool = nn.MaxPool3d(kernel_size=2, stride=2)
        
        # 1x1 convolutions for channel dimension adjustment
        self.adjust1 = nn.Conv3d(3, 30, kernel_size=(1, 1, 1), stride=1, padding=0)
        self.adjust2 = nn.Conv3d(30, 60, kernel_size=(1, 1, 1), stride=1, padding=0)
        self.adjust3 = nn.Conv3d(60, 120, kernel_size=(1, 1, 1), stride=1, padding=0)
        self.adjust4 = nn.Conv3d(120, 240, kernel_size=(1, 1, 1), stride=1, padding=0)
        
        # Fully connected layer
        self.fc = nn.Linear(691200, 2)  # Adjust the input features to match your flattened tensor


    def forward(self, x):
        # Initial block with skip connection
        identity = self.adjust1(x)  # Match the channel dimensions after conv2
        out = F.relu(self.conv1(x))
        out = F.relu(self.conv2(out))
        out = out + identity  # Add the skip connection
        out = self.pool(out)

        # The second block with skip connection
        identity = self.adjust2(out)  # Match the channel dimensions after conv4
        out = F.relu(self.conv3(out))
        out = F.relu(self.conv4(out))
        out = out + identity  # Add the skip connection
        out = self.pool(out)

        # Repeat for the remaining blocks
        identity = self.adjust3(out)  # Match the channel dimensions after conv6
        out = F.relu(self.conv5(out))
        out = F.relu(self.conv6(out))
        out = out + identity  # Add the skip connection
        out = self.pool(out)

        identity = self.adjust4(out)  # Match the channel dimensions after conv8
        out = F.relu(self.conv7(out))
        out = F.relu(self.conv8(out))
        out = out + identity  # Add the skip connection
        out = self.pool(out)

        # Flatten and pass through the fully connected layer
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out



"""## Create Model and Define Hyperparameters"""

# model instantiation
model = Basic3DCNN()

# Hyperparameters
num_epochs = 8
best_val_loss = float('inf')
patience = 3
early_stop_counter = 0
lr = 0.001

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=lr)
scheduler = lr_scheduler.StepLR(optimizer, step_size = 2, gamma = 0.75)

wandb.watch(model, log='all', log_freq=10)

#Log the parameters (this is strictly for logging to wandb, it doesn't change anything in the model)
# wandb.config = {
#   "learning_rate": lr,
#   "last lr" : scheduler.get_last_lr(),
#   "epochs": num_epochs,
#   "batch_size": 2
# }


"""## Train Model"""

# Training Loop
for epoch in range(num_epochs):

    start_time = time.time()

    model.train()  # Set model to training mode
    running_loss = 0.0
    train_corrects = 0

    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        optimizer.zero_grad()
        inputs = inputs.permute(0, 2, 1, 3, 4)  # Adjust dimensions
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        _, preds = torch.max(outputs, 1)
        train_corrects += torch.sum(preds == labels.data)

    scheduler.step()
    train_loss = running_loss / len(train_loader)
    train_accuracy = train_corrects.double() /len(train_loader.dataset)

    # Log training loss
    wandb.log({"epoch": epoch, "train_loss": running_loss / len(train_loader), "Train Accuracy": train_accuracy})

    # Validation Phase
    model.eval()  # Set model to evaluation mode
    val_loss = 0.0
    val_corrects = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs = inputs.permute(0, 2, 1, 3, 4)  # Adjust dimensions
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            val_corrects += torch.sum(preds == labels.data)

    end_time = time.time()
    epoch_time = end_time - start_time
    val_loss /= len(val_loader)
    val_accuracy = val_corrects.double() / len(val_loader.dataset)
    wandb.log({"val_loss": val_loss, "val_accuracy": val_accuracy})

    print(f'Epoch [{epoch+1}/{num_epochs}], Time: {epoch_time: .2f} seconds, Train Loss: {running_loss / len(train_loader)}, Train Accuracy :  {train_accuracy} Val Loss: {val_loss}, Val Accuracy: {val_accuracy}')

    # Early Stopping and Save best Model
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        early_stop_counter = 0  # Reset counter

        # Ensure the directory exists before saving the model
        os.makedirs(model_save_dir, exist_ok=True)

        # Save the best model
        torch.save(model.state_dict(), model_save_path)

    else:
        early_stop_counter += 1
        if early_stop_counter >= patience:
            print("Early stopping triggered")
            break

"""## Test Model"""

# Load the best model for testing
model.load_state_dict(torch.load(model_save_path))

# Testing Phase
test_loss = 0.0
test_corrects = 0
model.eval()  # Set model to evaluation mode

#Initialize list to store true labels and predicted probabilities
true_labels = []
predicted_probabilities = []

with torch.no_grad():
    for inputs, labels in test_loader:
        inputs = inputs.permute(0, 2, 1, 3, 4) #.to(device)  # Adjust dimensions
        labels = labels #.to(device)
        outputs = model(inputs)

        #Calculate loss
        loss = criterion(outputs, labels)
        test_loss += loss.item()

        #Get Predicted probabilities and true labels
        probabilities = torch.sigmoid(outputs)
        predicted_probabilities.extend(probabilities[:,1].cpu().numpy())
        true_labels.extend(labels.cpu().numpy())

        #Calculate Correct predictions
        _, preds = torch.max(outputs, 1)
        test_corrects += torch.sum(preds == labels.data)

#Calculate average test loss and accuracy
test_loss /= len(test_loader)
test_accuracy = test_corrects.double() / len(test_loader.dataset)

"""## Evaluate Results"""

# Calculate confusion matrix
true_labels = np.array(true_labels)
predicted_labels = np.array(predicted_probabilities) > 0.5
cm = confusion_matrix(true_labels, predicted_labels)

# Calculate ROC curve
fpr, tpr, thresholds = roc_curve(true_labels, predicted_probabilities)
roc_auc = auc(fpr, tpr)

# Calculate sensitivity and specificity
sensitivity = cm[1, 1] / (cm[1, 0] + cm[1, 1])
specificity = cm[0, 0] / (cm[0, 0] + cm[0, 1])

# Log metrics and artifacts to wandb
wandb.log({"test_loss": test_loss, "test_accuracy": test_accuracy, "roc_auc": roc_auc, "sensitivity": sensitivity, "specificity": specificity})

# Log confusion matrix as an image
plt.figure(figsize=(8, 6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.xticks([0, 1], ['Relaxed', 'Hold Breath'])
plt.yticks([0, 1], ['Relaxed', 'Hold Breath'])
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, format(cm[i, j], 'd'), horizontalalignment="center", color="white" if cm[i, j] > cm.max() / 2 else "black")
plt.tight_layout()
confusion_matrix_image_path = "confusion_matrix.png"
plt.savefig(confusion_matrix_image_path)
wandb.log({"confusion_matrix": wandb.Image(confusion_matrix_image_path)})

# Log ROC curve
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
roc_curve_image_path = "roc_curve.png"
plt.savefig(roc_curve_image_path)
wandb.log({"roc_curve": wandb.Image(roc_curve_image_path)})

# Print and save the ROC AUC
print("ROC AUC:", roc_auc)

print(f'Test Loss: {test_loss}, Test Accuracy: {test_accuracy}')