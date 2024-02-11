import os
from typing import List
import traceback

def read_log_files(log_file: str) -> List[str]:
    video_files = []
    
    try:
        with open(log_file, "r") as file:
            log_content = [line for line in file.read().split("\n") if line]
            video_files.append(log_content)
    except FileNotFoundError:
        print(f"File not found: {log_file}")

    return video_files

def extract_info_from_filepath(filepaths: List[str]) -> List[dict]:
    all_videos = []
    
    file_info_from_path = {
        0: "first name",
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
            filepath_parts = os.path.normpath(filepath).split(os.sep)[-splice_stop:]

            patient_info = {tag: filepath_parts[i] for i, tag in file_info_from_path.items() if i < splice_stop}

            # Combine information from filepath and default parameters
            patient_full_info = {**default_video_info, **patient_info}
            patient_full_info["local path"] = filepath

            all_videos.append(patient_full_info)  # Save to list
        except Exception:
            traceback.print_exc()
            print(f"Error processing file: {filepath}")

    return all_videos