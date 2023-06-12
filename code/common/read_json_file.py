import json


def read_json_file(json_file_path: str) -> dict:
    """
    Read a json file and return a dictionary
    :param json_file_path: path to json file
    :return: dictionary
    """
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    return data
