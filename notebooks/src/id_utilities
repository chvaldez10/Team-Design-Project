ALIAS_ID = {
    "Rachael B": "1",
    "Sara": "2",
    "Kate": "3",
    "Nick": "4",
    "Daniel": "5",
    "Illia": "6",
    "Melissa": "7",
    "Karlii": "8",
    "Eddy": "9",
    "John McNeil": "10",
    "Farooq": "11",
    "Krystyn": "12",
    "Jay": "13",
    "Frank": "14",
    "Arun": "15",
    "Riyan": "16",
    "Joseph": "17",
    "John Brunton": "18",
    "Illia2": "19",
    "Frank2": "20"
}

def get_alias(patient_info: dict, camera: str) -> str:
    """
    Retrieves an alias based on the patient's information and camera type.

    Args:
    patient_info (dict): A dictionary containing patient information.
    camera (str): The type of camera ('rgb' or 'thermal').

    Returns:
    str: The alias ID for the patient. If the camera is 'rgb' and the ID is not found in ALIAS_ID, it returns '?'.
         If the 'ID' key is missing in patient_info, returns 'Unknown'.
    """
    try:
        patient_id = patient_info["ID"]
    except KeyError:
        return "Unknown"

    if camera == "rgb":
        return ALIAS_ID.get(patient_id, "?")
    
    if camera == "thermal":
        return patient_id