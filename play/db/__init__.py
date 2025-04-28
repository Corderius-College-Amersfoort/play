"""A simple database system for storing data in a JSON file."""

import json
import os

FILENAME = "database.json"

JSON_DATA = None

if not os.path.exists(FILENAME):
    with open(FILENAME, "w", encoding="utf-8") as write_f:
        write_f.write("{}")

with open(FILENAME, "r", encoding="utf-8") as read_file:
    data = read_file.read()
    JSON_DATA = json.loads(data)


def get_data(key):
    """Get a value from the database.
    :param key: The key to get the value from, for which the : is a delimiter for nested values.
    """
    keys = key.split(":")
    value = JSON_DATA
    for k in keys:
        value = value.get(k, None)
    return value


def set_data(key, value):
    """Set a value in the database.
    :param key: The key to set the value to, for which the : is a delimiter for nested values.
    :param value: The value to set.
    """
    keys = key.split(":")
    target = JSON_DATA
    for k in keys[:-1]:
        if k not in target:
            raise KeyError(f"Key {k} not found in {target}")
        target = target[k]
    target[keys[-1]] = value

    with open(FILENAME, "w", encoding="utf-8") as write_file:
        write_file.write(json.dumps(JSON_DATA))
