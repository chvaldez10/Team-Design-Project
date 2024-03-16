import os
from typing import List, Tuple, Optional
import torch
from itertools import product
from torchvision.transforms import Compose
from torch.utils.data import Dataset
from PIL import Image

from src.dataset.breathing_dataset_config import DatasetConfig

BLANKET_STATUS = ["With Blankets", "Without Blankets"]
DISTANCE_MEASURES = ["2 Meters", "3 Meters"]
BREATHING_LABELS = ["Hold Breath", "Relaxed"]

class BreathingDataset(Dataset):
    def __init__(self, config: DatasetConfig):
        """
        Initializes the dataset.
        """
        self.root_dir = config.root_dir
        self.blanket_condition = config.blanket_condition
        self.distance = config.distance
        self.transform = config.transform
        self.max_frames = config.max_frames
        self.samples: List[Tuple[List[str], int]] = []

        self._generate_samples()

    def _generate_samples(self) -> None:
        conditions = BLANKET_STATUS if self.blanket_condition is None else [self.blanket_condition]
        distances = DISTANCE_MEASURES if self.distance is None else [self.distance]
        for condition, dist, label in product(conditions, distances, BREATHING_LABELS):
            self._add_samples_for_condition_distance_label(condition, dist, label)

    def _add_samples_for_condition_distance_label(self, condition: str, distance: str, label: str) -> None:
        label_path = os.path.join(self.root_dir, condition, distance, label)
        for subject_path in os.listdir(label_path):
            subject_full_path = os.path.join(label_path, subject_path)
            if os.path.isdir(subject_full_path):
                images = sorted([img for img in os.listdir(subject_full_path) if img.endswith(".jpg")], key=lambda x: int(x.split(".")[0]))
                images = images[:self.max_frames]
                image_paths = [os.path.join(subject_full_path, img) for img in images]
                self.samples.append((image_paths, 0 if label == "Hold Breath" else 1))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        images_path, label = self.samples[idx]
        images = [Image.open(img_path).convert("RGB") for img_path in images_path]

        if self.transform:
            images = [self.transform(image) for image in images]
        
        if len(images) < self.max_frames:
            padding = [torch.zeros_like(images[0]) for _ in range(self.max_frames - len(images))]
            images += padding
        
        images_stack = torch.stack(images)
        return images_stack, label