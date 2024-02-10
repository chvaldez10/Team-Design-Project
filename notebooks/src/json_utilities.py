import json
from typing import List, Dict

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


def restructure_json_file(metadata: List[Dict]) -> None:
    """
    Rearrange entries in each dictionary within a list in a json file.

    This function modifies each dictionary in the given list in a json file in-place.

    Args:
    json_filename (list): A list of dictionaries containing metadata.

    Returns:
    None: This function modifies the json file structure in-place and returns None.
    """

    # Define an empty list to store the new folder structures
    new_structures = []

    # Iterate over each dictionary in the original JSON data
    for index, entry in enumerate(metadata, start=1):
        # Define the new structure for each dictionary
        new_structure = {
            entry["blanket"]: {
                entry["breathing"]: {
                    entry["distance"]: {
                        # Use the string representation of i as the key
                        str(index): entry
                    }
                }
            }
        }
        # Append the new structure to the list
        new_structures.append(new_structure)

    # Convert the list of new structures to JSON format
    return new_structures