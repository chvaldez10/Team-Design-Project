import cv2
import os
def is_png_corrupted(file_path: str) -> bool:
    """
    Checks if a PNG file is corrupted.

    Parameters:
    file_path (str): Path to the PNG file.

    Returns:
    bool: True if the file is corrupted, False otherwise.
    """
    try:
        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        return image is None
    except Exception:
        return True

def find_corrupted_png_files(folder_path: str) -> list:
    """
    Finds all corrupted PNG files in a folder.

    Parameters:
    folder_path (str): Path to the folder to search.

    Returns:
    list: A list of paths to corrupted PNG files.
    """
    corrupted_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".png"):
                file_path = os.path.join(root, file)
                if is_png_corrupted(file_path):
                    corrupted_files.append(file_path)
    
    return corrupted_files

def report_corrupted_files(corrupted_files: list):
    """
    Prints the paths of corrupted files.

    Parameters:
    corrupted_files (list): A list of paths to corrupted files.
    """
    if corrupted_files:
        print("Corrupted PNG files found:")
        for file_path in corrupted_files:
            print(file_path)