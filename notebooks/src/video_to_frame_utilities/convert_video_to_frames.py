BREATHING_LABELS = ["Hold Breath", "Relaxed"]

def video_to_frames_driver(rgb_metadata: dict, client_schema: dict, blanket_status: list, distances: list, new_fps_string: str, new_fps: int, user_drive: str) -> list[str]:
    """
    Driver code to converts videos of multiple patients to frames.
    """
    visited_folders = {}
    video_folder_list = []

    for blanket in blanket_status:
        for distance in distances:
            for patient_id, patient_data in rgb_metadata[blanket][distance].items():
                print(patient_data)

    # for blanket_status in all_patients.items():
    #     try:
    #         frames_folder = process_patient(patient_info, level, new_fps, user_drive, visited_folders)
    #         video_folder_list.append(frames_folder)
    #     except Exception as e:
    #         traceback.print_exc()
    #         print(f'''{type(e)}: {e} for video {patient_info["filename"]}''')
    #     # break  

    # return visited_folders