import json
from typing import List, Dict
import copy

CLIENT_SCHEMA = {
    "Without Blankets": {
        "Hold Breath": {
            "2 Meters": {},
            "3 Meters": {}
        },
        "Relaxed": {
            "2 Meters": {},
            "3 Meters": {}
        }
    },
    "With Blankets": {
        "Hold Breath": {
            "2 Meters": {},
            "3 Meters": {}
        },
        "Relaxed": {
            "2 Meters": {},
            "3 Meters:": {}
        }
    },
}

DESIRED_VIDEO_DATA = ["frames", "length", "old fps", "alias", "local path", "ID", "filename"]

def switch_dictionary_values(key1: str, key2: str, patient_information: list) -> None:
    """
    Swap the values of two specified keys in each dictionary within a list.

    This function modifies each dictionary in the given list in-place. It swaps the values
    of the specified keys (key1 and key2) for each dictionary.

    Args:
    key1 (str): The first key whose value is to be swapped.
    key2 (str): The second key whose value is to be swapped.
    patient_information (list): A list of dictionaries where the swap will occur.

    Returns:
    None: This function modifies the list in-place and returns None.
    """
    for patient in patient_information:
        patient[key1], patient[key2] = patient[key2], patient[key1]

def restructure_metadata(patient_metadata: List[Dict]) -> Dict:
    """
    Restructures a list of patient metadata dictionaries to match a predefined schema, 
    avoiding direct modification of global variables and handling missing keys gracefully.

    Args:
        patient_metadata (List[Dict]): A list of dictionaries containing patient metadata.

    Returns:
        Dict: A new dictionary structured according to `CLIENT_SCHEMA`, populated with patient data.
    """
    # Deep copy the schema to avoid modifying the global variable
    new_structures = copy.deepcopy(CLIENT_SCHEMA)

    # Iterate over each dictionary in the patient metadata
    for index, patient_data in enumerate(patient_metadata, start=1):
        blanket_status = patient_data.get("blanket", "Without Blankets")
        breathing_status = patient_data.get("breathing", "Relaxed")
        distance = patient_data.get("distance", "2 Meters")

        # Initialize patient_video_data with the required fields
        patient_video_data = {key: patient_data.get(key) for key in DESIRED_VIDEO_DATA}

        if blanket_status in new_structures and breathing_status in new_structures[blanket_status] and distance in new_structures[blanket_status][breathing_status]:
            new_structures[blanket_status][breathing_status][distance][str(index)] = patient_video_data
        else:
            print(f"Invalid configuration for patient {index}: {patient_data}")

    return new_structures