from typing import List

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