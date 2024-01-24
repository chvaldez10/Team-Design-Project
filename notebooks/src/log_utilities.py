import os
import re
from typing import List

def get_patient_id(curr_dir: str) -> List[str]:
    try:
        patient_names = [folder_content for folder_content in os.listdir(curr_dir) if os.path.isdir(os.path.join(curr_dir, folder_content))]
        return patient_names
    except Exception as e:
        print(f"An error occurred: {e}")

def display_print():
    print("hi")

def filter_filenames(video_filenames: List[str], keyword: str) -> List[str]:
    """
    Filter out filenames that contain a specific keyword.
    """
    keyword_pattern = r"\b{}\b".format(re.escape(keyword))
    return [filename for filename in video_filenames if not re.search(keyword_pattern, filename, flags=re.IGNORECASE)]

def get_video_filenames(patient_path: str, current_level: int, max_level: int) -> List[str]:
    """
    Recursively collect video file paths from a given directory up to a specified level.
    """
    if current_level > max_level:
        return []

    file_paths = []
    for entry in os.scandir(patient_path):
        if entry.is_file():
            file_paths.append(entry.path)
        elif entry.is_dir():
            deeper_paths = get_video_filenames(entry.path, current_level + 1, max_level)
            file_paths.extend(deeper_paths)

    return file_paths

def write_filtered_filenames_to_log(file_paths: List[str], log_file: str) -> None:
    """
    Write a list of file paths to a log file.
    """
    print(log_file)
    with open(log_file, "a") as file:
        for path in file_paths:
            file.write(f"{path}\n")

def log_patient_video_files(root_dir: str, save_dir: str, log_filename: str, keywords: List[str], patient_list: List[str], max_level: int) -> None:
    """
    Process files for each patient, filtering and saving the filenames to a log file.
    """
    log_file = os.path.join(save_dir, f"{log_filename}.log").replace("\\", "/")

    if os.path.exists(log_file):
        os.remove(log_file)

    for patient_name in patient_list:
        patient_folder = os.path.join(root_dir, patient_name)
        all_patient_files = get_video_filenames(patient_folder, 0, max_level)

        for keyword in keywords:
            all_patient_files = filter_filenames(all_patient_files, keyword)

        write_filtered_filenames_to_log(all_patient_files, log_file)