import json
from datetime import datetime


def static_function_test(event, context):
    parameters = json.loads(event["body"])
    convert_json_to_array(parameters["array"])


def convert_json_to_array(json_from_api):
    array = []
    for element in json_from_api:
        array.append(element["id"])
    return array


# Convert string to datetime
def str_to_dtime(string_from_api):
    return datetime.strptime(string_from_api, '%d/%m/%Y %H:%M:%S')


def test(string):
    print(string)
