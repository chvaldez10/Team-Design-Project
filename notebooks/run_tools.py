# import libraries
import os
import sys
from dotenv import load_dotenv

# udf
from src.reader_utilities import load_json
from src.folder_utilities import create_folders_from_schema

json_dir = "../records/JSON/"
schema_dir = json_dir + "/schema"
curr_dir = os.getcwd()

# load root directory
dotenv_path = os.path.join(curr_dir, ".env")
load_dotenv(dotenv_path)
root_path = os.getenv("ROOT_FOLDER")
input(f"Is this the right directory - {root_path}?")

# Check if at least one argument is provided
if len(sys.argv) > 1:
    first_param = sys.argv[1]
    print(f"First parameter: {first_param}")
else:
    exit()

# load export path
export_path = first_param

client_schema = load_json(schema_dir, "client_schema.json")
create_folders_from_schema(client_schema, export_path)