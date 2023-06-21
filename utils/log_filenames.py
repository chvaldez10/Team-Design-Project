"""
    Gets the filenames of desired video files and stores them in log files.
    
    Usage: python log_filename.py
"""

import os
import re
import warnings

# local path
ROOT_PATH = "E:/Christian/DI_centre_structured"

def get_video_filenames(patient_path:str, level=0) -> None:
    file_paths = []

    os.chdir(patient_path)
    if level < 4:
        for entry in os.scandir(patient_path):
            if entry.is_file():
                file_paths.append(entry.path)
            elif entry.is_dir():
                file_paths.extend(get_video_filenames(entry.path, level+1))

    return file_paths

def get_patient_id(curr_dir:str) -> None:
    os.chdir(curr_dir)
    # patient_names = [folder_content for folder_content in os.listdir() if not folder_content.endswith(".mp4")]
    patient_names = [folder_content for folder_content in os.listdir() if os.path.isdir(folder_content)]
    return patient_names

def filter_filenames(video_filenames:list[str], keyword:str) -> list[str]:
    filtered_filenames = []
    for filename in video_filenames:
        if not re.search(r"\b{}\b".format(keyword), filename, flags=re.IGNORECASE):
            filtered_filenames.append(filename)
    return filtered_filenames

def save_filenames(root_dir:str, save_dir:str, video_name:str, keywords:list[str], patient_list:list[str]) -> None:
    log_file = f"{save_dir}/{video_name}.log"
    log_file = log_file.replace("\\", "/")

    if os.path.exists(log_file):
        os.remove(log_file)

    for patient_count, patient_name in enumerate(patient_list):
        patient_folder = root_dir + "/" + patient_name
        all_patient_mp4_files = get_video_filenames(patient_folder)
        filtered_filenames = all_patient_mp4_files

        for word in keywords:
            filtered_filenames = filter_filenames(filtered_filenames, word)

        with open(log_file, "a") as mp4_data:
            for mp4_file in filtered_filenames:
                mp4_data.write(f"{mp4_file}\n")

###########################################################
#
#            Main Loop
#
##########################################################

warnings.filterwarnings("ignore")

def main():
    repo_dir = os.getcwd()

if __name__ == "__main__":
    main()