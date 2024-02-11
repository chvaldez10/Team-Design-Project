import traceback
import pandas as pd
from typing import List
import os

def get_video_frame_paths(local_path: str, level: str) -> List[str]:
    """
    Constructs and returns paths related to video frames.

    Parameters:
    local_path (str): The local file path of the video.
    level (str): The detail level for the frames.

    Returns:
    List[str]: A list containing the folder path for frames and the video folder path.
    """
    video_folder, video_filename_with_ext = os.path.split(local_path)
    video_filename = os.path.splitext(video_filename_with_ext)[0]
    folder_path = os.path.join(video_folder, f"frames_{video_filename}_{level}")
    return [folder_path, video_folder]

def process_patient(patient_info, level, new_fps, user_drive, visited_folders):
    """
    Processes the video-to-frame conversion for a single patient.
    """
    video_path = patient_info["local path"]
    old_fps = int(patient_info["old fps"])

    frames_folder, video_folder = get_video_frame_paths(video_path, level)

    frames_to_pick = resample_and_validate_frames(old_fps, new_fps)
    patient_id = ""
    process_video_frames(video_path, frames_folder, frames_to_pick, new_fps, patient_id)
    check_drive_usage(user_drive)

    return frames_folder

def resample_and_validate_frames(old_fps, new_fps):
    """
    Resamples frames based on old and new fps, and validates the frame count.

    Args:
    - old_fps (int): The original frames per second of the video.
    - new_fps (int): The new frames per second to resample the video to.

    Returns:
    - list: List of frames to pick.

    Raises:
    - ValueError: If the number of frames to pick does not equal new fps.
    """
    frames_to_pick = resample_frames(old_fps, new_fps, 1)
    if len(frames_to_pick) != new_fps:
        raise ValueError("Number of frames to pick is not equal to new fps")
    return frames_to_pick

def process_video_frames(video_path, frames_folder, frames_to_pick, new_fps, patient_id):
    """
    Converts a video to frames based on specified parameters.

    Args:
    - video_path (str): Path to the video file.
    - frames_folder (str): Path to the folder to save the frames.
    - frames_to_pick (list): List of frames to pick from the video.
    - new_fps (int): The new frames per second.
    - patient_id (str): The patient's identifier.

    Prints:
    - Information about the frame processing.
    """
    frame_frequency = pd.Index(frames_to_pick, name="frames").value_counts()
    set_counter, save_counter, true_frames = run_video_to_frame(video_path, frames_folder, frame_frequency, new_fps, patient_id, False)
    print(f"\nSet counter: {set_counter}, save counter: {save_counter}, frame counter: {true_frames}\n\n"+ "-"*50)
    find_corrupted_png_files(frames_folder)

def convert_video_to_frame(all_patients: dict, level: str, new_fps: int, user_drive: str) -> list[str]:
    """
    Converts videos of multiple patients to frames.

    Args:
    - all_patients (dict): A dictionary of all patients and their video information.
    - level (str): The level of detail required for frame paths.
    - new_fps (int): The new frames per second to resample the videos.
    - user_drive (str): The drive to check for available storage.

    Returns:
    - list[str]: A list of paths to folders containing frames for each patient.

    Note:
    - This function stops after processing the first patient. Remove 'break' to process all.
    """
    visited_folders = {}
    video_folder_list = []

    for json_index, patient_info in all_patients.items():
        try:
            frames_folder = process_patient(patient_info, level, new_fps, user_drive, visited_folders)
            video_folder_list.append(frames_folder)
        except Exception as e:
            traceback.print_exc()
            print(f'''{type(e)}: {e} for video {patient_info["filename"]}''')
        # break  

    return visited_folders