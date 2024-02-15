from itertools import product

from src.video_to_frame_utilities.process_patient import process_patient
from src.video_to_frame_utilities.video_conversion_config import VideoConversionConfig

BREATHING_LABELS = ["Hold Breath", "Relaxed"]

def video_to_frames_driver(config: VideoConversionConfig) -> list[str]:
    """
    Driver code to converts videos of multiple patients to frames.
    """
    visited_folders = {}
    video_folder_list = []

    for blanket_status, distance, breathing_label in product(config.blanket_statuses, config.distance_measures, BREATHING_LABELS):
        video_data = config.rgb_metadata[blanket_status][distance][breathing_label]
        
        # skip if metadata is empty
        if not video_data:
            continue
        
        print(f"Metadata for {blanket_status}, {distance}, {breathing_label}:")

        for video_id, video_data in video_data.items():
            try:
                print(f"  processing {video_id}: {video_data}")
                # process_patient()
            except KeyError as e:
                print(f"Key error accessing metadata: {video_id}")