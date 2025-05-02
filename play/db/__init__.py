"""A simple database system for storing data in a JSON file."""

import json
import os
from ..io.logging import play_logger


def correct_filename(filename: str):
    """checks whether a given filename for a JSON database is correctly formatted
    :param filename: the  filename to be checked"""
    try:
        filename = str(filename)
        if filename[-5:] != '.json':
            filename = f"{filename}.json"
    except Exception as e:
        play_logger.error(f"an error occured {e}",exc_info=True)
    return filename

def new_dataset(filename: str = "database.json", path: str = None):
    """Creates a new database.
    :param filename: the name of the new database
    :param path: (optional) a specified path when the database is not to be created in the executing folder"""
    try:
        filename = correct_filename(filename)
        if not path:
            if not os.path.exists(filename):
                with open(filename, "w", encoding="utf-8") as write_f:
                    write_f.write("{}")
            else:
                raise FileExistsError("File already exists")
        elif path:
            if os.path.exists(path):
                if not os.path.exists(f"{path}\\{filename}"):
                    with open(f"{path}\\{filename}", "w", encoding="utf-8") as write_f:
                        write_f.write("{}")
                else:
                    raise FileExistsError("File already exists")
            else:
                raise FileNotFoundError("Given path is incorrect")
    except Exception as e:
        play_logger.error(f"An error occured:\n{e}", exc_info=True)


def get_full_data(filename:str, path: str = None):
    """requests the full data of a database
    :param filename: name of the file which is supposed to be read"""
    try:
        if path:
            if os.path.exists(path):
                filename = correct_filename(f"{path}\\{filename}")
            else:
                raise FileNotFoundError("given path is incorrect")
        else:
            filename = correct_filename(filename)
        JSON_DATA = _get_JSON_DATA(filename)
        return JSON_DATA
    except Exception as e:
        play_logger.error(f"An error occured\nError e: {e}", exc_info=True)
        return None

def _get_JSON_DATA(filename:str):
    """helper function which reads JSON-data from a file"""
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as read_file:
                data= read_file.read()
                JSON_DATA = json.loads(data)
                return JSON_DATA
        else:
            raise FileNotFoundError(f"File {filename} was not found")
    except Exception as e:
        play_logger.error(f"An error occured:\n{e}", exc_info=True)
        return None

def clear_dataset(filename:str):
    """Clear a specified database.
    :param filename: The name of the file to clear
    """
    try:
        with open(filename, "w", encoding="utf-8") as write_f:
            write_f.write("{}")
    except Exception as e:
        play_logger.error(f"An error occured\nError e: {e}", exc_info=True)

def get_data(key, filename:str):
    """Get a value from the database.
    :param key: The key to get the value from, for which the : is a delimiter for nested values.
    :param filename: The name of the file to set the data to
    """
    try:
        filename = correct_filename(filename)
        keys = key.split(":")
        value = _get_JSON_DATA(filename)
        for k in keys:
            value = value[k]
        return value
    except Exception as e:
        play_logger.error(f"An error occured\nError e: {e}", exc_info=True)
        return None


def set_data(key, value):
    """Set a value in the database.
    :param key: The key to set the value to, for which the : is a delimiter for nested values.
    :param value: The value to set.
    """
    keys = key.split(":")
    JSON_DATA = _get_JSON_DATA("database.json")
    target = JSON_DATA
    for k in keys[:-1]:
        if k not in target:
            raise KeyError(f"Key {k} not found in {target}")
        target = target[k]
    target[keys[-1]] = value

    with open("database.json", "w", encoding="utf-8") as write_file:
        write_file.write(json.dumps(JSON_DATA))

def set_data_extended(filename: str, input_path: str, value: str|int|float|list|dict = None):
    """
    Add data to a JSON file at a nested path.

    :param filename: Name of the JSON file
    :param input_path: The key to set the value to, for which the : is a delimiter for nested values, last (or only) value is key
    :param value: The value to insert at the specified path

    """
    try:
        filename = correct_filename(filename)
        with open(filename, "r", encoding="utf-8") as read_file:
            old_data = json.load(read_file)

        path_list = input_path.split(":")
        if path_list[-1] == '':
            path_list.pop()
        current = old_data
        
        for key in path_list[:-1]:
            if key not in current:
                current[key] = {}
            elif key in current:
                if type(current[key]) is not dict:
                    current[key] = {} 
            current = current[key]

        current[path_list[-1]] = value
        
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(old_data, file, indent=4)
    except Exception as e:
        play_logger.error(f"An error occured\n Error e: {e}", exc_info=True)