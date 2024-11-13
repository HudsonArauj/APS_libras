import json



def get_data(file_path):
    # read the json file
    with open(file_path, 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data

