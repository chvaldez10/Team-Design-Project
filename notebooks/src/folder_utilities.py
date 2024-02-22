from pathlib import Path

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
    export_path = Path(base_path)
    
    # Iterate through the schema to find conditions
    for blanket_status, distances in client_schema.items():
        for distance, conditions in distances.items():
            for condition in conditions.keys():
                # Create a test file for each condition
                dir_path = export_path / blanket_status / distance / condition
                print(dir_path)

                # Create a directory for the condition
                dir_path.mkdir(parents=True, exist_ok=True)

                print(dir_path)

                # Test file
                export_file = dir_path / "del_me.txt"
                with export_file.open("w") as test_data:
                    test_data.write(f"Test file for {condition}")