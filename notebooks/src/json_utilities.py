import json
from typing import List, Dict
import copy
from importlib import reload

# reload for module caching
import src.id_utilities
reload(src.id_utilities)

# import custom functions
from src.id_utilities import get_patient_id

CLIENT_SCHEMA = {
    "Without Blankets": {
        "2 Meters": {
            "Hold Breath": {},
            "Relaxed": {}
        },
        "3 Meters": {
            "Hold Breath": {},
            "Relaxed": {}
        }
    },
    "With Blankets": {
        "2 Meters": {
            "Hold Breath": {},
            "Relaxed": {}
        },
        "3 Meters": {
            "Hold Breath": {},
            "Relaxed": {}
        }
    },
}

DESIRED_VIDEO_DATA = ["frames", "length", "old fps", "local path", "first name", "filename"]

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
        alias = patient_data.get("alias", "?")
        blanket_status = patient_data["blanket"]
        distance = patient_data["distance"]
        breathing_status = patient_data["breathing"]
        patient_id = get_patient_id(alias, blanket_status, distance, breathing_status, index)

        # Initialize patient_video_data with the required fields
        patient_video_data = {key: patient_data.get(key) for key in DESIRED_VIDEO_DATA}

        if blanket_status in new_structures and distance in new_structures[blanket_status] and breathing_status in new_structures[blanket_status][distance]:
            new_structures[blanket_status][distance][breathing_status][patient_id] = patient_video_data
        else:
            print(f"Invalid configuration for patient {index}: {patient_data}")

    return new_structures