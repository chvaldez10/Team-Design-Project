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