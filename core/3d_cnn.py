import re
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import os
from typing import List, Tuple
from itertools import product
from PIL import Image
import random
from datetime import datetime

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

# -------------------------------------------------------------------------------- #
#                                                                                  #
#                               Main Function                                      #
#                                                                                  #
# -------------------------------------------------------------------------------- #

def main():
    start_time = datetime.now()

    print("Initializing dataset and data loader ...")

    transform = transforms.Compose([
        transforms.Resize((180, 320)),
        transforms.ToTensor(),
    ])

    train_dataset_without_blankets = BreathingDataset('/work/TALC/enel645_2024w/design_project_yene/rgb_10-fps/Train', blanket_condition='Without Blankets', distance=None, transform=transform)
    val_dataset_without_blankets = BreathingDataset('/work/TALC/enel645_2024w/design_project_yene/rgb_10-fps/Validation', blanket_condition='Without Blankets', distance=None, transform=transform)
    test_dataset_without_blankets = BreathingDataset('/work/TALC/enel645_2024w/design_project_yene/rgb_10-fps/Test', blanket_condition='Without Blankets', distance=None, transform=transform)

    train_loader = DataLoader(train_dataset_without_blankets, batch_size=1, shuffle=True)  # Shuffle for training - this shuffles the samples (i.e. sets of frames, rather than individual frames.)
    val_loader = DataLoader(val_dataset_without_blankets, batch_size=1, shuffle=False)  # No shuffle for validation
    test_loader = DataLoader(test_dataset_without_blankets, batch_size=1, shuffle=False)  # No shuffle for testing

    dataset_loader_end_time = datetime.now()
    delta = dataset_loader_end_time - start_time
    formatted_time = str(delta).split('.')[0]

    print("len train_dataset_without_blankets =", len(train_dataset_without_blankets.samples))

    print("Time taken to finish loading dataset: ", formatted_time)

    print("Starting training...")
    
    print("Training complete.")

if __name__ == "__main__":
    main()