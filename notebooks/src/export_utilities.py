
from typing import List

def write_filtered_filenames_to_log(file_paths: List[str], log_file: str) -> None:
    """
    Write a list of file paths to a log file.
    """
    print(log_file)
    with open(log_file, "a") as file:
        for path in file_paths:
            file.write(f"{path}\n")