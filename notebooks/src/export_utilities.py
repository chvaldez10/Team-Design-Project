
from typing import List
import json
import pandas as pd

def write_filtered_filenames_to_log(file_paths: List[str], log_file: str) -> None:
    """
    Write a list of file paths to a log file.
    """
    try:
        with open(log_file, "w") as file:
            for path in file_paths:
                file.write(f"{path}\n")
        print(f"exported to: {log_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def export_to_json(patients: list[dict], filename: str) -> None:
    """
    Exports a list of patient dictionaries to a JSON file.

    Args:
    patients (list[dict]): A list of dictionaries containing patient data.
    filename (str): The name of the file to which the data will be exported.

    Returns:
    None: The function writes data to a file but does not return any value.
    """
    if not filename.endswith('.json'):
        filename += '.json'

    try:
        with open(filename, "w") as json_data:
            json.dump(patients, json_data, indent=2)
        print(f"Data successfully exported to {filename}")
    except Exception as e:
        print(f"An error occurred while exporting data: {e}")

def export_to_excel(patient_info: dict, filename: str) -> None:
    """
    Exports patient information to an Excel file.

    Args:
    patient_info (dict): A dictionary containing patient data.
    filename (str): The filename for the exported Excel file.

    Returns:
    None: The function writes data to an Excel file but does not return any value.
    """
    # Ensure the filename ends with .xlsx
    if not filename.endswith('.xlsx'):
        filename += '.xlsx'

    try:
        # Convert dictionary to DataFrame
        patient_df = pd.DataFrame.from_dict(patient_info, orient='index')
        patient_df = patient_df.drop(columns=["local path"])

        # Set multi-level index
        new_df = patient_df.set_index(["ID", "distance", "breathing", "blanket", "filename"])

        # Export to Excel
        new_df.to_excel(filename)
        print(f"Data successfully exported to {filename}")
    except Exception as e:
        print(f"An error occurred while exporting to Excel: {e}")