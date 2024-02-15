from itertools import product

from importlib import reload
import src.video_to_frame_utilities.video_conversion_config
reload(src.video_to_frame_utilities.video_conversion_config)
from src.video_to_frame_utilities.video_conversion_config import VideoConversionConfig

BREATHING_LABELS = ["Hold Breath", "Relaxed"]

def video_to_frames_driver(config: VideoConversionConfig) -> list[str]:
    """
    Driver code to converts videos of multiple patients to frames.
    """
    visited_folders = {}
    video_folder_list = []

    for blanket_status, distance, breathing_label in product(config.blanket_statuses, config.distance_measures, BREATHING_LABELS):
        try:
            video_data = config.rgb_metadata[blanket_status][distance][breathing_label]
            
            if not video_data:
                continue
            
            print(f"Metadata for {blanket_status}, {distance}, {breathing_label}:")
            for key, value in video_data.items():
                print(f"  {key}: {value}")
        except KeyError as e:
            print(f"Key error accessing metadata: {e}")

    # for blanket_status in all_patients.items():
    #     try:
    #         frames_folder = process_patient(patient_info, level, new_fps, user_drive, visited_folders)
    #         video_folder_list.append(frames_folder)
    #     except Exception as e:
    #         traceback.print_exc()
    #         print(f'''{type(e)}: {e} for video {patient_info["filename"]}''')
    #     # break  

    # return visited_folders