import os

def get_patient_id(curr_dir:str) -> None:
    patient_names = [folder_content for folder_content in os.listdir(curr_dir) if os.path.isdir(folder_content)]
    return patient_names