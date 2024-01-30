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
