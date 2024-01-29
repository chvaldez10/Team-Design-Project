from typing import List, Dict
import json
import os

def parse_line_by_line(log_file: str) -> List[str]:
    """
    Parse filename line by line and return list
    """
    
    try:
        with open(log_file, "r") as file:
            file_content = [line for line in file.read().split("\n") if line]
    except FileNotFoundError:
        print(f"File not found: {log_file}")

    return file_content

def load_json(json_dir: str, filename: str) -> Dict:
    """
    Loads a JSON file from a specified directory and filename.

    Args:
    json_dir (str): The directory where the JSON file is located.
    filename (str): The name of the JSON file to be loaded.

    Returns:
    dict: The contents of the JSON file. Returns an empty dictionary if the file is not found or invalid.
    """
    # Normalize the path and filename
    full_path = os.path.normpath(os.path.join(json_dir, filename))

    try:
        with open(full_path, "r") as json_data:
            return json.load(json_data)
    except FileNotFoundError:
        print(f"Error: The file {full_path} does not exist.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file {full_path} is not a valid JSON.")
        return {}