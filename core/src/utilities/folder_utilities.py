from pathlib import Path
import logging

def set_folder(save_folder: str) -> None:
    """
    Ensures the specified folder exists. If the folder doesn't exist, it is created.
    Regardless, its contents are removed to ensure it's empty.

    Args:
    save_folder (str): The path to the folder.
    """
    folder_path = Path(save_folder)
    folder_path.mkdir(parents=True, exist_ok=True)  # Create folder if not exists; no-op if exists.
    
    for file_path in folder_path.iterdir():
        try:
            if file_path.is_file():
                file_path.unlink()  # Remove file
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}")

def create_folders_from_schema(client_schema: dict, base_path: str) -> None:
    """
    Create a nested folder structure based on a given schema and base path.

    This function iterates through a client schema dictionary to create a
    directory tree. For each condition specified in the schema, it also creates
    a test file within the corresponding folder.

    Parameters:
    - client_schema (dict): A nested dictionary representing the folder structure
      schema. Expected format: {<status>: {<distance>: {<condition>: ...}}}.
    - base_path (str): The base path where the folder structure will be created.

    Returns:
    - None
    """
    # Convert base path to a Path object for easier path manipulation
    export_path = Path(base_path)
    
    # Iterate through the schema to create directories and test files
    for blanket_status, distances in client_schema.items():
        for distance, conditions in distances.items():
            for condition in conditions:
                # Construct the directory path
                dir_path = export_path / blanket_status / distance / condition
                # Ensure the directory exists
                dir_path.mkdir(parents=True, exist_ok=True)

                # Create a test file in the directory
                create_test_file(dir_path, condition)

def create_test_file(directory: Path, condition: str) -> None:
    """
    Creates a test file within a given directory for a specific condition.

    Parameters:
    - directory (Path): The directory where the test file will be created.
    - condition (str): The condition name to be included in the test file's content.

    Returns:
    - None
    """
    test_file_path = directory / "del_me.txt"
    with test_file_path.open("w") as file:
        file.write(f"Test file for {condition}")