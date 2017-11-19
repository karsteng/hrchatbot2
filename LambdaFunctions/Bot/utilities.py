import os
import json


def get_json(filename):
    """Load json file.
    :param string filepath: Path to file.
    """
    filepath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        filename)
    with open(filepath) as fh:
        return json.loads(fh.read())


def load_enumeration_values(type_def_file):
    json = get_json(type_def_file)
    return tuple(v["value"] for v in json["enumerationValues"])
