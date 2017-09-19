import csv
import re
import os

PATTERN = re.compile(r'^[0-9\.]+$')

def to_num(arg):
    if isinstance(arg, list):
        return [to_num(row) for row in arg]
    elif PATTERN.match(arg):
        return float(arg)

    return arg


def read_file(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(dir_path, file_name), 'r') as file:
        result = list(csv.reader(file, delimiter=';'))
        return to_num(result)

