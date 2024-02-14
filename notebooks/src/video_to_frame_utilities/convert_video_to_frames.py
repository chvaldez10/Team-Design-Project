def video_to_frames_driver(all_patients: dict, level: str, new_fps: int, user_drive: str) -> list[str]:
    """
    Driver code to converts videos of multiple patients to frames.

    Args:
    - all_patients (dict): A dictionary of all patients and their video information.
    - level (str): The level of detail required for frame paths.
    - new_fps (int): The new frames per second to resample the videos.
    - user_drive (str): The drive to check for available storage.

    Returns:
    - list[str]: A list of paths to folders containing frames for each patient.
    """
    visited_folders = {}
    video_folder_list = []

    for json_index, patient_info in all_patients.items():
        try:
            frames_folder = process_patient(patient_info, level, new_fps, user_drive, visited_folders)
            video_folder_list.append(frames_folder)
        except Exception as e:
            traceback.print_exc()
            print(f'''{type(e)}: {e} for video {patient_info["filename"]}''')
        # break  

    return visited_folders