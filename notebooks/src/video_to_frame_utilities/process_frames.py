import cv2
import os
import pandas as pd
from importlib import reload

import src.video_to_frame_utilities.save_frame as save_Frame
reload(save_Frame)

from src.video_to_frame_utilities.frames_conversion_config import FrameConversionConfig
from src.utilities.folder_utilities import set_folder
from src.video_to_frame_utilities.save_frame import save_frame, update_counters, validate_frame_count

def video_to_frame(config: FrameConversionConfig) -> list[int]:
    """
    Converts a video into frames based on specified frequencies and saves them to a folder.
    """
    
    # assign paths
    video_path = os.path.normpath(config.root_path + config.local_video_path)
    save_folder = os.path.normpath(config.export_path + "/" + config.video_id)
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        raise IOError(f"Cannot open video file at {video_path}")

    # Prepare frame list and variables
    frames_to_pick = list(config.frame_frequency.keys())
    expected_frame_count = config.new_fps * config.video_duration
    frame_counters = {"pick": 0, "save": 0, "set": 0, "true": 0}

    # Print initial processing information
    print(f"\n  Saving frames to: {save_folder}\n  Picking frames: {frames_to_pick} per set\n  Expected number of frames: {expected_frame_count} ({config.new_fps}FPS * {config.video_duration}s).")

    # Ensure save folder is ready
    set_folder(save_folder)

    # Process video
    while frame_counters["set"] < config.video_duration:
        success, frame = video.read()
        if not success:
            break

        if frame_counters["pick"] in frames_to_pick:
            save_frame(video, frame, config.frame_frequency, frame_counters, config.video_id, save_folder)

        update_counters(frame_counters, config.old_fps)

        # for testing
        if frame_counters["true"] > config.frame_limit and config.debug_mode:
            print(f"  Limit set to {config.frame_limit} frames for testing purposes.")
            break

    video.release()

    # Post-processing validation and timing
    validate_frame_count(frame_counters["save"], expected_frame_count)
    return [frame_counters[key] for key in ["set", "save", "true"]]