import cv2
import os
from timeit import default_timer as timer
import pandas as pd

from src.video_to_frame_utilities.frames_conversion_config import FrameConversionConfig

DEBUGGING_MODE = True

def video_to_frame(config: FrameConversionConfig) -> list[int]:
    """
    Converts a video into frames based on specified frequencies and saves them to a folder.
    """
    
    # assign paths
    video_path = os.path.normpath(config.root_path + config.local_video_path)
    save_folder = ""


    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise IOError(f"Cannot open video file at {video_path}")

    # Prepare frame list and variables
    frames_to_pick = list(config.frame_frequency.keys())
    expected_frame_count = config.new_fps * config.video_duration
    frame_counters = {'pick': 0, 'save': 0, 'set': 0, 'true': 0}

    # Print initial processing information
    print(f"\nSaving frames to: {save_folder}\nPicking frames: {frames_to_pick} per set\nExpected number of frames: {expected_frame_count} ({config.new_fps}FPS * {config.video_duration}s).")

    # # Ensure save folder is ready
    # set_folder(save_folder)

    # # Process video
    # start_time = timer()
    # while frame_counters['set'] < video_duration:
    #     success, frame = video.read()
    #     if not success:
    #         break

    #     if frame_counters['pick'] in frames_to_pick:
    #         save_frame(video, frame, frame_frequency, frame_counters, patient_id, save_folder)

    #     update_counters(frame_counters, vid_fps)

    #     # for testing
    #     if frame_counters['true'] > FRAME_LIMIT and debug_mode:
    #         print(f"\nLimit set to {FRAME_LIMIT} frames for testing purposes.")
    #         break

    # video.release()

    # # Post-processing validation and timing
    # end_time = timer()
    # validate_frame_count(frame_counters['save'], expected_frame_count)
    # print(f"\nDone in {end_time - start_time} seconds.")

    # return [frame_counters[key] for key in ['set', 'save', 'true']]
    return [0, 0, 0]