from typing import List
import numpy as np

def resample_frames(old_fps: int, new_fps: int, start: int) -> List[int]:
    """
    Resamples the number of frames from an old frame rate to a new frame rate. 
    This function can handle both upsampling and downsampling.

    Parameters:
    old_fps (int): The original frames per second.
    new_fps (int): The new frames per second to resample to.
    start (int): The starting frame index.

    Returns:
    List[int]: A list of frame indices after resampling.

    Raises:
    ValueError: If old_fps or new_fps are non-positive integers.
    """
    if old_fps <= 0 or new_fps <= 0:
        raise ValueError("old_fps and new_fps must be positive integers.")

    original_frame_indices = np.arange(start, old_fps, dtype=int)
    interpolated_frame_positions = np.linspace(start, old_fps - 1, new_fps)
    nearest_frame_indices = np.round(interpolated_frame_positions).astype(int)
    resampled_frame_indices = np.take(original_frame_indices, nearest_frame_indices, mode='wrap')

    return resampled_frame_indices.tolist()