
from typing import List

def write_filtered_filenames_to_log(file_paths: List[str], log_file: str) -> None:
    """
    Write a list of file paths to a log file.
    """
    try:
        with open(log_file, "w") as file:
            for path in file_paths:
                file.write(f"{path}\n")
        print(f"exported to: {log_file}")
    except Exception as e:
        print(f"An error occurred: {e}")