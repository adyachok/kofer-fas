import re

from flask import request


def process_request_value_name(name):
    return '_'.join([string.lower() for string in
                     re.split('([A-Z][a-z]*)', name) if string.strip()])


def parse_request() -> object:
    data = {}
    if request.method == 'GET':
        for key, val in request.args.to_dict().items():
            data[process_request_value_name(key)] = val
    else:
        for key, val in request.values.to_dict().items():
            data[process_request_value_name(key)] = val
        data['files'] = request.files
    return data
