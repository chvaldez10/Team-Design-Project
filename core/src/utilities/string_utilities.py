from typing import List

def replace_substring_in_list(list_of_strings: List[str], string_to_replace: str, string_to_replace_it_with: str) -> None:
    """
    Replace a specified substring with another substring in each string of a list.

    This function modifies each string in the given list in-place. It searches for a
    specified substring (string_to_replace) in each string and replaces it with
    another specified substring (string_to_replace_it_with).

    Args:
    list_of_strings (List[str]): The list of strings to be modified.
    string_to_replace (str): The substring that needs to be replaced.
    string_to_replace_it_with (str): The substring to replace with.

    Returns:
    None: This function modifies the list in-place and returns None.
    """
    for index, list_item in enumerate(list_of_strings):
        list_of_strings[index] = list_item.replace(string_to_replace, string_to_replace_it_with)