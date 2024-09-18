import json
import os

FILENAME = 'database.json'

json_data = None

if not os.path.exists(FILENAME):
    with open(FILENAME, 'w') as write_f:
        write_f.write('{}')

with open(FILENAME, 'r') as read_file:
    data = read_file.read()
    json_data = json.loads(data)


def get_data(key):
    """Get a value from the database.
    :param key: The key to get the value from, for which the : is a delimiter for nested values.
    """
    global json_data
    keys = key.split(':')
    value = json_data
    for k in keys:
        value = value[k]
    return value


def set_data(key, value):
    """Set a value in the database.
    :param key: The key to set the value to, for which the : is a delimiter for nested values.
    :param value: The value to set.
    """
    global json_data
    keys = key.split(':')
    target = json_data
    for k in keys[:-1]:
        if k not in target:
            raise KeyError(f'Key {k} not found in {target}')
        target = target[k]
    target[keys[-1]] = value
    print(json_data)

    with open(FILENAME, 'w') as write_file:
        write_file.write(json.dumps(json_data))