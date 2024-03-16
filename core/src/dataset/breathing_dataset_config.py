from typing import Optional
from torchvision.transforms import Compose

class BreathingDatasetConfig:
    def __init__(self, root_dir: str, blanket_condition: Optional[str] = None, distance: Optional[str] = None, transform: Optional[Compose] = None, max_frames: int = 100):
        self.root_dir = root_dir
        self.blanket_condition = blanket_condition
        self.distance = distance
        self.transform = transform
        self.max_frames = max_frames