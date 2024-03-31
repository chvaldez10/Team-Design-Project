"""
This script is designed for training and testing a 3D Convolutional Neural Network (CNN) model
for image recognition tasks.

Command-Line Options:
  --train : Train the model using the training and validation datasets. This will also save the 
            trained model to a specified path. If this option is selected, the script will perform
            training operations including model training and validation.

  --test  : Test the model using the test dataset. This option requires that a trained model is
            available and specified in the script. If this option is selected, the script will
            perform testing operations and output the performance metrics of the model on the test dataset.

Both options can be used together to first train the model and then test it without needing to run
the script twice. If no option is specified, the script will not perform any operations.

Examples:
  To train the model:
  python your_script_name.py --train

  To test the model:
  python your_script_name.py --test

  To train and then test the model:
  python your_script_name.py --train --test

Note: Ensure that the dataset paths, model save path, and any other configurations are correctly
set within the script before running it.
"""

import re
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import torch.optim as optim
import os
from typing import List, Tuple
from itertools import product
from PIL import Image
import random
from datetime import datetime
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import lr_scheduler
import wandb

# Define Checkpoint Information
model_save_dir = './model_checkpoints'
current_time = datetime.now().strftime('%Y%m%d-%H%M%S')
model_filename = f'best_model_{current_time}.pth'
model_save_path = os.path.join(model_save_dir, model_filename)

# Define Number of frames used for each sample.
max_frames = 100
BLANKET_STATUS = ["With Blankets", "Without Blankets"]
DISTANCE_MEASURES = ["2 Meters", "3 Meters"]
BREATHING_LABELS = ["Hold Breath", "Relaxed"]

def extract_number(filename: str) -> int:
    match = re.search(r"(\d+)\.jpg$", filename)
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
        """Retrieves and sorts images in a subject's directory. """
        frames_path = os.listdir(subject_path)
        images = [os.path.join(subject_path, img) for img in frames_path if img.endswith(".jpg")]
        images = sorted(images, key=extract_number)
        return images

    def __len__(self) -> int:
        """Returns the total number of samples."""
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        """Retrieves a sample and its label, applying transformations as needed."""
        images_path, label = self.samples[idx]
        images = [self._load_image(img_path) for img_path in images_path]

        if random.random() > 0.5:
            images = [self._horizontal_flip(img) for img in images]

        if len(images) < self.max_frames:
            images += [torch.zeros_like(images[0]) for _ in range(self.max_frames - len(images))]

        if len(images) > self.max_frames:
            # If there are more than 100 frames, select 100 frames from a random spot
            start_idx = random.randint(0, len(images) - self.max_frames)
            images = images[start_idx:start_idx + self.max_frames]

        return torch.stack(images), label

    def _load_image(self, img_path: str) -> torch.Tensor:
        """Loads an image, converts it to RGB, and applies transformations."""
        image = Image.open(img_path).convert("RGB")
        return self.transform(image) if self.transform else image

    def _horizontal_flip(self, img: torch.Tensor) -> torch.Tensor:
        """Applies horizontal flip to an image."""
        return torch.flip(img, dims=[2])

def initialize_dataset_and_loader(train_path: str, val_path: str, test_path: str, transform: transforms.Compose) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Initializes the dataset and data loaders for training, validation, and testing.
    """
    start_time = datetime.now()
    print("Initializing dataset and data loader ...")

    train_dataset = BreathingDataset(train_path, blanket_condition='Without Blankets', distance=None, transform=transform)
    val_dataset = BreathingDataset(val_path, blanket_condition='Without Blankets', distance=None, transform=transform)
    test_dataset = BreathingDataset(test_path, blanket_condition='Without Blankets', distance=None, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=1, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)

    dataset_loader_end_time = datetime.now()
    delta = dataset_loader_end_time - start_time
    formatted_time = str(delta).split('.')[0]

    print(f"Dataset and loader initialization completed in {formatted_time}.")
    print(f"len train_dataset_without_blankets = {len(train_dataset.samples)}")

    return train_loader, val_loader, test_loader

class Basic3DCNN(nn.Module):
    def __init__(self):
        super(Basic3DCNN, self).__init__()
        self.conv1 = nn.Conv3d(in_channels=3, out_channels=30, kernel_size=(3, 3, 3), padding=1)  # (100, 320, 180)
        self.conv2 = nn.Conv3d(30, 30, kernel_size=(3, 3, 3), padding=1)  # stride 2 reduces dimensions by half (50, 160, 90)
        self.conv3 = nn.Conv3d(in_channels=30, out_channels=60, kernel_size=(3, 3, 3), padding=1)
        self.conv4 = nn.Conv3d(60, 60, kernel_size=(3, 3, 3), padding=1)  # (25, 80, 45)
        self.conv5 = nn.Conv3d(in_channels=60, out_channels=120, kernel_size=(3, 3, 3), padding=1)
        self.conv6 = nn.Conv3d(120, 120, kernel_size=(3, 3, 3), padding=1)  # (12, 40, 22.5 = 22)
        self.conv7 = nn.Conv3d(in_channels=120, out_channels=240, kernel_size=(3, 3, 3), padding=1)
        self.conv8 = nn.Conv3d(240, 240, kernel_size=(3, 3, 3), padding=1)  # (6, 20, 11)
        self.pool = nn.MaxPool3d(kernel_size=2, stride=2)  # (3, 10, 5)
        self.dropout = nn.Dropout3d(0.3)
        self.fc = nn.Linear(316800, 2)
        # d5e3c7 * 3 * 10 * 5  = 36000 but it says its value above? batch size makes a difference
    
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = self.pool(x)
        x = F.relu(self.conv5(x))
        x = F.relu(self.conv6(x))
        x = self.pool(x)
        x = F.relu(self.conv7(x))
        x = F.relu(self.conv8(x))
        x = self.pool(x)
        # x = x.flatten(start_dim=1)
        x = x.view(-1,316800)
        # x = self.dropout(x)
        x = self.fc(x)
        return x

def train_model(model: Basic3DCNN, train_loader: DataLoader, val_loader: DataLoader, num_epochs: int, model_save_path: str, patience: int, device: torch.device):
    """
    Trains a given model with specified parameters and data loaders, ensuring all data is moved to the specified device.
    """
    model = model.to(device)
    lr = 0.0005
    best_val_loss = float('inf')
    early_stop_counter = 0
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.6)

    wandb.init(
        project="3d-cnn-team-design",
        name="test-run",
        config={"learning_rate": lr, "architecture": "2d_cnn", "dataset": "calgary_di", "epochs": num_epochs}
    )

    for epoch in range(num_epochs):
        model.train()  # Set the model to training mode
        running_loss = 0.0
        train_corrects = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            inputs = inputs.permute(0, 2, 1, 3, 4)  # Adjust dimensions if necessary
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            train_corrects += torch.sum(preds == labels.data)

        scheduler.step()  # Update learning rate
        train_loss = running_loss / len(train_loader)
        train_accuracy = train_corrects.double() / len(train_loader.dataset)
        wandb.log({"epoch": epoch, "train_loss": running_loss / len(train_loader), "Train Accuracy": train_accuracy})

        model.eval()  # Set the model to evaluation mode
        val_loss = 0.0
        val_corrects = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                inputs = inputs.permute(0, 2, 1, 3, 4)  # Adjust dimensions if necessary
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, preds = torch.max(outputs, 1)
                val_corrects += torch.sum(preds == labels.data)

        val_loss /= len(val_loader)
        val_accuracy = val_corrects.double() / len(val_loader.dataset)

        wandb.log({"val_loss": val_loss, "val_accuracy": val_accuracy})

        # Early stopping and model checkpointing
        if val_loss < best_val_loss:
            torch.save(model.state_dict(), model_save_path)
            best_val_loss = val_loss
            early_stop_counter = 0  # Reset the counter
        else:
            early_stop_counter += 1
            if early_stop_counter >= patience:
                print("Early stopping triggered.")
                break

def test_model(model: Basic3DCNN, test_loader: DataLoader, model_save_path: str, device: torch.device):
    """
    Test the model with the given test data loader and criterion.
    """
    # Load the best model for testing
    model.load_state_dict(torch.load(model_save_path))

    # Testing Phase
    model.eval()  # Set model to evaluation mode
    criterion = nn.CrossEntropyLoss()
    test_loss = 0.0
    test_corrects = 0
    
    # Initialize list to store true labels and predicted probabilities
    true_labels = []
    predicted_probabilities = []

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.permute(0, 2, 1, 3, 4)  # Adjust dimensions if necessary
            inputs, labels = inputs.to(device), labels.to(device)
            
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            test_loss += loss.item()

            # Get Predicted probabilities and true labels
            probabilities = torch.sigmoid(outputs)
            predicted_probabilities.extend(probabilities[:,1].cpu().numpy())
            true_labels.extend(labels.cpu().numpy())

            # Calculate Correct predictions
            _, preds = torch.max(outputs, 1)
            test_corrects += torch.sum(preds == labels.data)

    # Calculate average test loss and accuracy
    test_loss /= len(test_loader)
    test_accuracy = test_corrects.double() / len(test_loader.dataset)

    return test_loss, test_accuracy, true_labels, predicted_probabilities

# -------------------------------------------------------------------------------- #
#                                                                                  #
#                               Main Function                                      #
#                                                                                  #
# -------------------------------------------------------------------------------- #

def main():
    transform = transforms.Compose([
        transforms.Resize((180, 320)),
        transforms.ToTensor(),
    ])

    train_path = "/work/TALC/enel645_2024w/design_project_yene/rgb_10-fps/Train"
    val_path = "/work/TALC/enel645_2024w/design_project_yene/rgb_10-fps/Validation"
    test_path = "/work/TALC/enel645_2024w/design_project_yene/rgb_10-fps/Test"

    train_loader, val_loader, test_loader = initialize_dataset_and_loader(train_path, val_path, test_path, transform)

    # model instantiation
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Basic3DCNN()
    model.to(device)

    train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        num_epochs=10,
        model_save_path='/home/christian.valdez/DI-Automated-Scripts/best_model/3d_cnn.pth',
        patience=3,
        device=device
    )

if __name__ == "__main__":
    main()