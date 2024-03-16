import re

def extract_number(filename: str) -> int:
    match = re.search(r"(\d+)\.jpg$", filename)
    if match:
        return int(match.group(1))
    return None