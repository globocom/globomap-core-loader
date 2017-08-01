import json


def open_json(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)
        return data
