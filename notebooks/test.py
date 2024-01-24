# import libraries
import os
import re
from dotenv import load_dotenv

# import custom functions
from src.log_utilities import get_patient_id, log_patient_video_files

# get file directory
curr_dir = os.getcwd()

# load root directory
dotenv_path = os.path.join(curr_dir, ".env")
load_dotenv(dotenv_path)
root_path = os.getenv("ROOT_FOLDER")
input(f"Is this the right directory - {root_path}?")

p3225_file_path = {
    "video folder" : "DI_CAMERA_P3225",
    "1st level" : ["Final"],
    "2nd level" : "Patient Name",
    "3rd level" : [2, 3],
    "4th level" : { "B": "With Blankets",
                        "WOB": "Without Blankets"}, 
    "5th level" : {"H" : "Hold Breath",
                    "R": "Relaxed"} 
}

fur_file_path = {
    "video folder" : "DI_THERMAL_FLIR",
    "1st level" : [""],
    "2nd level" : "Patient Number",
    "3rd level" : [2, 3],
    "4th level" : { "H": "Hold Breath",
                        "R": "Relaxed"}, 
    "5th level" : { "B": "With Blankets",
                        "WOB": "Without Blankets"} 
}

""" get filenames from folder names """

video_folder = p3225_file_path["video folder"]
all_videos_folder = root_path + "/" + video_folder + "/" + p3225_file_path["1st level"][0]
# patient_names = get_patient_id(all_videos_folder)
get_patient_id(all_videos_folder)