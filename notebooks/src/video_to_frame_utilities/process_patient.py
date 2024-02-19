import pandas as pd
from importlib import reload

import src.video_to_frame_utilities.frame_sampler as frame_sampler
import src.video_to_frame_utilities.process_frames as process_frames
import src.video_to_frame_utilities.frames_conversion_config as frames_conversion_config
import src.metadata_utilities

reload(frame_sampler)
reload(process_frames)
reload(frames_conversion_config)
reload(src.metadata_utilities)

from src.video_to_frame_utilities.frame_sampler import resample_and_validate_frames
from src.video_to_frame_utilities.process_frames import video_to_frame
from src.video_to_frame_utilities.frames_conversion_config import FrameConversionConfig
from src.metadata_utilities import calculate_video_duration

# Global constants
DEBUGGING_MODE = True
CROP_COORDINATES = [700.4810791015625, 300, 1766.735595703125, 1080.0]

def process_patient(root_path: str, video_id: str, video_data: dict, new_fps: int):
    """
    Processes the video-to-frame conversion for a single patient.
    """
    # extract metadata
    old_fps = int(video_data["old fps"])
    frame_count = int(video_data["frames"])
    video_duration = calculate_video_duration(old_fps, frame_count)

    # local path
    local_video_path = video_data["local path"]
    
    # frame data
    frames_to_pick = resample_and_validate_frames(old_fps, new_fps)
    frame_frequency = pd.Index(frames_to_pick, name="frames").value_counts()
    
    # load values
    config = FrameConversionConfig(root_path, local_video_path, video_id, frame_frequency, new_fps, CROP_COORDINATES, DEBUGGING_MODE)

    # call vid to frames
    set_counter, save_counter, true_frames = video_to_frame(config)

    print(f"  Set counter: {set_counter}, save counter: {save_counter}, frame counter: {true_frames}\n\n" + "-"*50)

    print(str(config))

    # check_drive_usage(user_drive)
    # find_corrupted_png_files(frames_folder)
    # return frames_folder