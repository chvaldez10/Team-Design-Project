import os
from typing import List, Tuple
from itertools import product
import torch
from torch.utils.data import Dataset
from PIL import Image

from src.dataset.breathing_dataset_config import BreathingDatasetConfig
from src.utilities.list_utilities import extract_number

BLANKET_STATUS = ["With Blankets", "Without Blankets"]
DISTANCE_MEASURES = ["2 Meters", "3 Meters"]
BREATHING_LABELS = ["Hold Breath", "Relaxed"]

class BreathingDataset(Dataset):
    def __init__(self, config: BreathingDatasetConfig):
        """Initializes the BreathingDataset with configuration."""
        self.root_dir = config.root_dir
        self.blanket_condition = config.blanket_condition
        self.distance = config.distance
        self.transform = config.transform
        self.max_frames = config.max_frames
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
        """Retrieves and sorts images in a subject's directory, limited by max_frames."""
        frames_path = os.listdir(subject_path)
        images = [os.path.join(subject_path, img) for img in frames_path if img.endswith(".jpg")]
        images = sorted(images, key=extract_number)
        return images[:self.max_frames]

    def __len__(self) -> int:
        """Returns the total number of samples."""
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        """Retrieves a sample and its label, applying transformations as needed."""
        images_path, label = self.samples[idx]
        images = [self._load_image(img_path) for img_path in images_path]

        if len(images) < self.max_frames:
            images += [torch.zeros_like(images[0]) for _ in range(self.max_frames - len(images))]
        
        return torch.stack(images), label

    def _load_image(self, img_path: str) -> torch.Tensor:
        """Loads an image, converts it to RGB, and applies transformations."""
        image = Image.open(img_path).convert("RGB")
        return self.transform(image) if self.transform else image
