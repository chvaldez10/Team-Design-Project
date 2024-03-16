from src.utilities.id_utilities import get_alias
import cv2
import os
from typing import Dict, List, Tuple
import re

# reload for module caching
from importlib import reload
import src.utilities.id_utilities
reload(src.utilities.id_utilities)

# Define alias IDs for train, validation, and test
TRAIN_ID = ["15", "5", "9", "11", "14",
            "6", "13", "18", "17", "16", "3", "1"]
VAL_ID = ["7", "4", "12"]
TEST_ID = ["8", "2"]

def extract_number(filename: str) -> int:
    match = re.search(r"(\d+)\.jpg$", filename)
    if match:
        return int(match.group(1))
    return None

def create_video_from_jpg(frames_folder: str, output_video_path: str, fps: int, frame_limit:int = None):
    """
    Creates a video from a series of JPG images in a specified folder.
    """
    try:
        frames = sorted([frame for frame in os.listdir(frames_folder) if frame.endswith('.jpg')], key=extract_number)
        
        if frame_limit is not None:
            frames = frames[:frame_limit]

        # list is empty
        if not frames:
            print(f"No JPG files found in the folder '{frames_folder}'.")
            return
        
        # read the first frame
        first_frame = cv2.imread(os.path.join(frames_folder, frames[0]))
        if first_frame is None:
            raise IOError(
                f"Failed to read the first image from '{frames_folder}'.")

        height, width, _ = first_frame.shape
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
        
        print(f"config: fps = {fps}, number of frames = {len(frames)}")
        try:
            for jpg_file in frames:
                img = cv2.imread(os.path.join(frames_folder, jpg_file))
                if img is None:
                    raise IOError(f"Failed to read '{jpg_file}' from '{frames_folder}'.")
                out.write(img)
        finally:
            out.release()

        print(f"Video successfully created at '{output_video_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_video_properties(mp4_file: str) -> Tuple:
    """
    Extracts properties from an MP4 video file.

    Args:
    mp4_file (str): The path to the MP4 file.

    Returns:
    tuple: A tuple containing the number of frames, frames per second (FPS),
           and the length of the video in seconds. Returns None if an error occurs.

    Raises:
    Exception: Any exception that occurs while processing the video file.
    """
    try:
        video = cv2.VideoCapture(mp4_file)
        fps = video.get(cv2.CAP_PROP_FPS)
        number_of_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        length = number_of_frames / fps
        video.release()
        return number_of_frames, fps, length
    except Exception as e:
        print(f"{type(e).__name__} occurred while processing {mp4_file}: {e}")
        return None


def add_video_properties(root_path: str, metadata: List[Dict], camera: str) -> List[Dict]:
    """
    Enhances patient metadata with video properties and alias based on camera type.

    Args:
    metadata (dict): A dictionary of patient metadata.
    camera (str): The type of camera used ('rgb' or 'thermal').

    Returns:
    dict: The enriched metadata with added video properties and aliases.
    """
    enriched_metadata = []
    # Define alias IDs for train, validation, and test

    for patient_id, patient_info in enumerate(metadata):
        try:
            video_path = root_path + patient_info.get("local path")
            if not video_path:
                raise ValueError(
                    f"Missing 'local path' for patient ID {patient_info['first name']}_{patient_id}")

            frames, fps, length_in_seconds = get_video_properties(video_path)
            alias = get_alias(patient_info, camera)

            # Split data based on client id
            if alias in TRAIN_ID:
                set_value = "Train"
            elif alias in VAL_ID:
                set_value = "Validation"
            elif alias in TEST_ID:
                set_value = "Test"

            patient_info.update({
                "frames": frames,
                "old fps": fps,
                "length": length_in_seconds,
                "alias": alias,
                "set": set_value
            })

            enriched_metadata.append(patient_info)

        except Exception as e:
            print(f"Error processing patient ID {patient_info['ID']}: {e}")

    return enriched_metadata
