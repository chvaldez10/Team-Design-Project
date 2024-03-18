from typing import List, Tuple

def get_sliding_window_indices(num_of_frames: int, window_size: int, step_size: int) -> List[Tuple[int, int]]:
    """
    Generate indices for sliding windows over a sequence.

    Args:
    num_of_frames (int): Total number of frames in the sequence.
    window_size (int): The size of each window.
    step_size (int): The step size between windows.

    Returns:
    List[Tuple[int, int]]: A list of tuples, where each tuple contains the start and end indices of a window.
    """
    if window_size > num_of_frames:
        raise ValueError("Window size cannot be larger than the number of frames.")

    return [(i, min(i + window_size, num_of_frames)) for i in range(0, num_of_frames - window_size + 1, step_size)]