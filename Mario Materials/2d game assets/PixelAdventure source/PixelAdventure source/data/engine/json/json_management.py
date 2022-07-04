import json


FILES_PATH = ""


def write(file_name, data):
    with open(FILES_PATH + file_name, 'w') as file:
        json.dump(data, file, indent=4)

def get_data(file_name) -> dict:
    with open(FILES_PATH + file_name, 'r') as file:
        return json.load(file)
