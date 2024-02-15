from importlib import reload
import src.video_to_frame_utilities.frame_sampler
reload(src.video_to_frame_utilities.frame_sampler)

from src.video_to_frame_utilities.frame_sampler import resample_and_validate_frames

def process_patient(video_id: str, video_data: dict, new_fps:int):
    """
    Processes the video-to-frame conversion for a single patient.
    """
    video_path = video_data["local path"]
    old_fps = int(video_data["old fps"])

    frames_to_pick = resample_and_validate_frames(old_fps, new_fps)
    print(f"picking frames {frames_to_pick}")
    
    process_video_frames(video_path, frames_folder, frames_to_pick, new_fps, patient_id)
    # check_drive_usage(user_drive)
    # return frames_folder