from typing import List
import numpy as np

def resample_frames(old_fps: int, new_fps: int, start: int) -> List[int]:
    """
    Resamples the number of frames from an old frame rate to a new frame rate.
    
    This function can handle both upsampling and downsampling frames.
    """
    if old_fps <= 0 or new_fps <= 0:
        raise ValueError("old_fps and new_fps must be positive integers.")

    original_frame_indices = np.arange(start, old_fps, dtype=int)
    interpolated_frame_positions = np.linspace(start, old_fps - 1, new_fps)
    nearest_frame_indices = np.round(interpolated_frame_positions).astype(int)
    resampled_frame_indices = np.take(original_frame_indices, nearest_frame_indices, mode='wrap')

    return resampled_frame_indices.tolist()

def resample_and_validate_frames(old_fps, new_fps):
    """
    Resamples frames based on old and new fps, and validates the frame count.
    """
    frames_to_pick = resample_frames(old_fps, new_fps, 1)
    if len(frames_to_pick) != new_fps:
        raise ValueError("Number of frames to pick is not equal to new fps")
    return frames_to_pick