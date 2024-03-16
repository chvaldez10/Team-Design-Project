import os
from typing import List, Tuple, Optional
import torch
from itertools import product
from torchvision.transforms import Compose
from torch.utils.data import Dataset
from PIL import Image

class BreathingDataset(Dataset):
    def __init__(self, root_dir: str, blanket_condition: Optional[str] = None, distance: Optional[str] = None, transform: Optional[Compose] = None, max_frames: int = 100):
        """
        Initializes the dataset.

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
        conditions = ['With Blankets', 'Without Blankets'] if self.blanket_condition is None else [self.blanket_condition]
        distances = ['2 Meters', '3 Meters'] if self.distance is None else [self.distance]
        labels = ['Hold Breath', 'Relaxed']

        for condition, dist, label in product(conditions, distances, labels):
            self._add_samples_for_condition_distance_label(condition, dist, label)

    def _add_samples_for_condition_distance_label(self, condition: str, distance: str, label: str) -> None:
        label_path = os.path.join(self.root_dir, condition, distance, label)
        for subject_path in os.listdir(label_path):
            subject_full_path = os.path.join(label_path, subject_path)
            if os.path.isdir(subject_full_path):
                images = sorted([img for img in os.listdir(subject_full_path) if img.endswith('.jpg')],
                                key=lambda x: int(x.split('.')[0]))
                images = images[:self.max_frames]
                image_paths = [os.path.join(subject_full_path, img) for img in images]
                self.samples.append((image_paths, 0 if label == 'Hold Breath' else 1))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        images_path, label = self.samples[idx]
        images = [Image.open(img_path).convert('RGB') for img_path in images_path]

        if self.transform:
            images = [self.transform(image) for image in images]
        
        if len(images) < self.max_frames:
            padding = [torch.zeros_like(images[0]) for _ in range(self.max_frames - len(images))]
            images += padding
        
        images_stack = torch.stack(images)
        return images_stack, label
