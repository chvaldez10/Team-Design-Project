import cv2
import os

def save_frame(video, frame, frame_frequency, counters, patient_id, folder):
    """
    Saves a given frame to the specified folder, updating counters accordingly.
    """
    for _ in range(frame_frequency.get(counters["pick"])):
        frame_name = f"{counters['save']}.png"
        cv2.imwrite(os.path.join(folder, frame_name), frame)
        counters["save"] += 1

def update_counters(counters, vid_fps):
    """
    Updates the frame processing counters.
    """
    counters["pick"] += 1
    counters["true"] += 1
    if counters["pick"] == vid_fps:
        counters["set"] += 1
        counters["pick"] = 0

def validate_frame_count(actual_count, expected_count):
    """
    Validates if the actual frame count matches the expected frame count.
    """
    if actual_count != expected_count:
        raise ValueError(f"Expected {expected_count} frames, but got {actual_count} frames")