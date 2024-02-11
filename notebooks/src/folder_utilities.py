from pathlib import Path

def set_folder(save_folder: str) -> None:
    """
    Ensures the specified folder exists and is empty.
    If the folder doesn't exist, it is created. If it exists, its contents are removed.

    Args:
    save_folder (str): The path to the folder.
    """
    folder_path = Path(save_folder)
    if not folder_path.is_dir():
        folder_path.mkdir(parents=True, exist_ok=True)
    else:
        try:
            for file_name in folder_path.iterdir():
                if file_name.is_file():
                    file_name.unlink()
        except OSError as e:
            print(f"Error: {e}")