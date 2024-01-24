import os
from typing import List
import traceback

def read_log_files(log_directory: str) -> List[List[str]]:
    video_files = []
    
    # Create a list of log file paths
    log_files = [os.path.join(log_directory, file) for file in os.listdir(log_directory) if file.endswith(".log")]

    for log_file_path in log_files:
        try:
            with open(log_file_path, "r") as file:
                # Exclude empty lines directly here
                log_content = [line for line in file.read().split("\n") if line]
                video_files.append(log_content)
        except FileNotFoundError:
            print(f"File not found: {log_file_path}")

    return video_files

def extract_info_from_filepath(filepaths: List[str]) -> List[dict]:
    all_videos = []
    file_info_from_path = {
        0: "ID",
        1: "distance",
        2: "blanket",
        3: "breathing",
        4: "filename"
    }

    default_video_info = {
        "frames": None,
        "length": None,
        "old fps": None,
        "alias": None,
        "local path": None,
    }

    splice_stop = 5

    for filepath in filepaths:
        try:
            # Use os.path for compatibility and readability
            filepath_parts = os.path.normpath(filepath).split(os.sep)[-splice_stop:]

            # Extract info from filepath
            patient_info = {tag: filepath_parts[i] for i, tag in file_info_from_path.items() if i < splice_stop}

            # Combine information from filepath and default parameters
            patient_full_info = {**default_video_info, **patient_info}
            patient_full_info["local path"] = filepath

            all_videos.append(patient_full_info)  # Save to list
        except Exception:
            traceback.print_exc()
            print(f"Error processing file: {filepath}")

    return all_videos