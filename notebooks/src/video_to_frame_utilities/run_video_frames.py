import cv2
from timeit import default_timer as timer

def run_video_to_frame(video_path: str, save_folder: str, frame_frequency: dict, new_fps: int, patient_id: str, debug_mode:bool) -> list[int]:
    """
    Converts a video into frames based on specified frequencies and saves them to a folder.

    Args:
    video_path (str): Path to the video file.
    save_folder (str): Folder to save the extracted frames.
    frame_frequency (dict): Frequency of frames to extract.
    new_fps (int): Target frames per second.
    patient_id (str): ID of the patient, used in naming frames.

    Returns:
    list[int]: List containing number of sets processed, frames saved, and true frames processed.
    """
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise IOError(f"Cannot open video file at {video_path}")

    # Extract video metadata
    vid_fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = frame_count // vid_fps

    # Prepare frame list and variables
    frames_to_pick = list(frame_frequency.keys())
    expected_frame_count = new_fps * video_duration
    frame_counters = {'pick': 0, 'save': 0, 'set': 0, 'true': 0}

    # Print initial processing information
    print(f"\nSaving frames to: {save_folder}\nPicking frames: {frames_to_pick} per set\nExpected number of frames: {expected_frame_count} ({new_fps}FPS * {video_duration}s).")

    # Ensure save folder is ready
    set_folder(save_folder)

    # Process video
    start_time = timer()
    while frame_counters['set'] < video_duration:
        success, frame = video.read()
        if not success:
            break

        if frame_counters['pick'] in frames_to_pick:
            save_frame(video, frame, frame_frequency, frame_counters, patient_id, save_folder)

        update_counters(frame_counters, vid_fps)

        # for testing
        if frame_counters['true'] > FRAME_LIMIT and debug_mode:
            print(f"\nLimit set to {FRAME_LIMIT} frames for testing purposes.")
            break

    video.release()

    # Post-processing validation and timing
    end_time = timer()
    validate_frame_count(frame_counters['save'], expected_frame_count)
    print(f"\nDone in {end_time - start_time} seconds.")

    return [frame_counters[key] for key in ['set', 'save', 'true']]