"""A bunch of random math functions."""

import pygame
import os


def _clamp(num, min_, max_):
    if num < min_:
        return min_
    if num > max_:
        return max_
    return num


class _Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, indices):
        if indices == 0:
            return self.x
        if indices == 1:
            return self.y
        raise IndexError()

    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self):
        return 2

    def __setitem__(self, i, value):
        if i == 0:
            self.x = value
        elif i == 1:
            self.y = value
        else:
            raise IndexError()

def search_file(start_directory, filename):
    """
    Search for a specified file from the start directory and return its full path.
    :param start_directory: The path to the starting directory from which the search starts
    :param filename: The name of the file to search for, also takes file name without file extension (e.g., "example.txt" or "example").
    :return: a list with either all filepaths which match exactly to the filename or a list with filepaths which match at least partially, and a dict with key:value pairs of filepath:filename where the filename either exactly matches the searched filename or partially matches the searched filename
    """
    partial_matching_fileslist = []
    partial_matching_filesdict = {}
    matchlist = []
    matchdict = {}
    if os.path.exists(start_directory):
        for dirpath, dirnames, filenames in os.walk(start_directory):
            for file in filenames:
                if file == filename:
                    matchlist.append(os.path.join(dirpath, file))
                    matchdict[os.path.join(dirpath, file)] = file
                file_parts_list = file.split(".")
                partial_filename = ""
                for part in file_parts_list:
                    partial_filename = partial_filename + part
                    if partial_filename.lower() == filename.lower():
                        if file not in partial_matching_filesdict and file not in matchdict: partial_matching_fileslist.append(os.path.join(dirpath, file)); partial_matching_filesdict[os.path.join(dirpath, file)] = file
    return partial_matching_fileslist, partial_matching_filesdict if len(matchlist) == 0 else matchlist, matchdict

def get_files_by_extension(start_directory, extension):
    """Search for all files with the specified extension in the given directory and its subdirectories"""
    matching_files = []
    for dirpath, dirnames, filenames in os.walk(start_directory):
        for filename in filenames:
            if filename.endswith(extension):
                matching_files.append(os.path.join(dirpath, filename))
    if matching_files:
        for file in matching_files:
            print(f"Found: {file}")
    else:
        print(f"No files with the {extension} extension were found.")
    
    return matching_files

def remove_files(file_list: list|str):
    """function that removes items in a list from the project directory
    :file_list either a list of the files to be removed, or a single file to be removed
    """
    if isinstance(file_list, list):
        for file in file_list:
            try:
                if os.path.exists(file):
                    os.remove(file)
                else:
                    pass
            except Exception as e:
                print(f"error e has occured while trying to remove file: {file}\nerror e:{e}")
    elif isinstance(file_list, str):
        try:
            if os.path.exists(file_list):
                os.remove(file_list)
        except Exception as e:
            print(f"error e has occured.\nerror e:{e}")
    elif not isinstance(file_list, (list, str)):
        raise TypeError(f"type file_list expected to be list or string, but is {type(file_list).__name__}")

def remove_dupes_in_list(list_input: list)-> list:
    non_dupe_list = []
    if isinstance(list_input, list):
        for item in list_input:
            if item not in non_dupe_list:
                non_dupe_list.append(item)
        return non_dupe_list
    elif not isinstance(list_input, list):
        return list_input
    
def color_name_to_rgb(name):
    """
    Turn an English color name into an RGB value.

    lightBlue
    light-blue
    light blue

    are all valid and will produce the rgb value for lightblue.
    """
    if isinstance(name, tuple):
        return name

    try:
        return pygame.color.THECOLORS[
            name.lower().strip().replace("-", "").replace(" ", "")
        ]
    except KeyError as exception:
        raise ValueError(
            f"""You gave a color name we didn't understand: '{name}'
Try using the RGB number form of the color e.g. '(0, 255, 255)'.
You can find the RGB form of a color on websites like this: https://www.rapidtables.com/web/color/RGB_Color.html\n"""
        ) from exception
