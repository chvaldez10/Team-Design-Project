import os
import json

def load_json(json_dir: str, filename: str) -> dict:
    # Remove leading slash if present in filename
    if filename.startswith("/"):
        filename = filename[1:]

    full_path = os.path.join(json_dir, filename)

    try:
        with open(full_path, "r") as json_data:
            return json.load(json_data)
    except FileNotFoundError:
        print(f"Error: The file {full_path} does not exist.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file {full_path} is not a valid JSON.")
        return {} 
    
def export_to_json(filename: str, all_patient_info: dict) -> None:
    patient_json = json.dumps(all_patient_info, indent=2)

    with open(filename, "w") as json_data:
        json_data.write(patient_json)