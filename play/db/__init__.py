"""A simple database system for storing data in a JSON file."""

import json
import os

class Database:
    def __init__(self, db_filename="database.json"):
        """
        Initialize the database with a JSON file.
        :param db_filename: The name of the JSON file to use as the database.
        """
        self.db_filename = db_filename
        self.data = {}

        if not os.path.exists(db_filename):
            with open(db_filename, "w", encoding="utf-8") as write_f:
                write_f.write("{}")

        with open(db_filename, "r", encoding="utf-8") as read_file:
            self.data = read_file.read()

    def get_data(self, key):
        """Get a value from the database.
        :param key: The key to get the value from, for which the : is a delimiter for nested values.
        """
        keys = key.split(":")
        value = self.data
        for k in keys:
            value = value.get(k, None)
        return value


    def set_data(self, key, value):
        """Set a value in the database.
        :param key: The key to set the value to, for which the : is a delimiter for nested values.
        :param value: The value to set.
        """
        keys = key.split(":")
        target = self.data
        for k in keys[:-1]:
            if k not in target:
                raise KeyError(f"Key {k} not found in {target}")
            target = target[k]
        target[keys[-1]] = value

        with open(self.db_filename, "w", encoding="utf-8") as write_file:
            write_file.write(json.dumps(self.data, indent=4))