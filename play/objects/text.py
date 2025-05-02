"""This module contains the Text class, which is a text string in the game."""

import os
import pygame
from .sprite import Sprite
from ..io import convert_pos
from ..utils import (
    color_name_to_rgb as _color_name_to_rgb,
    search_file
    )
from ..io.logging import play_logger
import requests
from ..db import *


executing_folder = os.getcwd()

used_fonts_pathlist = []

class Text(Sprite):
    def __init__(  # pylint: disable=too-many-arguments
        self,
        words="hi :)",
        x=0,
        y=0,
        font="default",
        font_size=50,
        color="black",
        angle=0,
        transparency=100,
        size=100,
        bold=False,
        italic=False,
        underlined=False,
        strikethrough=False,
        git_token=False
    ):
        if not pygame.font.get_init(): pygame.font.init()
        super().__init__()
        self._font = font
        self._font_size = font_size
        self._git_token = git_token

        self._pygame_font = self._load_font(font, font_size, git_token)

        self._words = words
        self._color = color

        self._x = x
        self._y = y

        self._bold = bold
        self._italic = italic
        self._underlined = underlined
        self._strikethrough = strikethrough

        self._size = size
        self._angle = angle
        self.transparency = transparency

        self._is_clicked = False
        self._is_hidden = False
        self.physics = None

        self._when_clicked_callbacks = []

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update()


    def update(self):
        """Update the text object."""
        if self._should_recompute:

            pos = convert_pos(self.x, self.y)
            self._pygame_font.set_bold(self._bold)
            self._pygame_font.set_italic(self._italic)
            self._pygame_font.set_underline(self._underlined)
            self._pygame_font.set_strikethrough(self._strikethrough)


            self._image = self._pygame_font.render(
                self._words, True, _color_name_to_rgb(self._color)
            )

            self.rect = self.image.get_rect()
            self.rect.topleft = (
                pos[0] - self.rect.width // 2,
                pos[1] - self.rect.height // 2,
            )

            super().update()

    def clone(self):
        return self.__class__(
            words=self.words,
            font=self.font,
            font_size=self.font_size,
            color=self.color,
            **self._common_properties(),
        )

    @property
    def words(self):
        """Get the words of the text object."""
        return self._words

    @words.setter
    def words(self, string):
        """Set the words of the text object."""
        self._words = str(string)
    
    @property
    def bold(self):
        """Check if the text object is bold"""
        return self._bold
    
    @bold.setter
    def bold(self, boolean):
        """Set the boldness of the text object"""
        if isinstance(boolean, bool):
            self._bold = boolean

    @property
    def italic(self):
        """Check if the text object is italic"""
        return self._italic
    
    @italic.setter
    def italic(self, boolean):
        """Set the italicness of the text object"""
        if isinstance(boolean, bool):
            self._italic = boolean

    @property
    def underlined(self):
        """Check if the text object is underlined"""
        return self._underlined
    
    @underlined.setter
    def underlined(self, boolean):
        """Change whether the text object is underlined"""
        if isinstance(boolean, bool):
            self._underlined = boolean
 
    @property
    def strikethrough(self):
        """Check if the text object is struck through"""
        return(self._strikethrough)

    @strikethrough.setter
    def strikethrough(self, boolean):
        """Change whether the text object is struck through"""
        if isinstance(boolean, bool):
            self._strikethrough = boolean

    @property
    def font(self):
        """Get the font of the text object."""
        return self._font

    @font.setter
    def font(self, font_name):
        """Set the font of the text object. This will load the font dynamically."""
        if isinstance(font_name, str):
            self._font = font_name
            self._pygame_font = self._load_font(font_name, self._font_size, self._git_token)

    @property
    def font_size(self):
        """Get the font size of the text object."""
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        """Set the font size of the text object."""
        self._font_size = size
        self._pygame_font = self._load_font(self._font, size)

    @property
    def color(self):
        """Get the color of the text object."""
        return self._color

    @color.setter
    def color(self, color_):
        """Set the color of the text object."""
        self._color = color_
    
    @property
    def git_token(self):
        """Get the used github token or returns false if none was provided"""
        return self._git_token
    
    @git_token.setter
    def git_token(self, git_token):
        if isinstance(git_token, str) or not git_token:
            self._git_token = git_token

    def _load_font(self, font_name, font_size, git_token):

        if len(font_name) == 0:
            play_logger.warning("font name is too short\nusing default font", exc_info=True)
            return pygame.font.Font(pygame.font.get_default_font(), font_size)
        
        if font_name.lower() == "none" or font_name == None or font_name.lower() == "arial.ttf" or font_name.lower() == "default" or font_name == "/path/to/font":
            return pygame.font.Font(pygame.font.get_default_font(), font_size)

        if os.path.exists(font_name) and font_name[-4:] == ".ttf":
            if font_name not in used_fonts_pathlist: used_fonts_pathlist.append(font_name)
            return pygame.font.Font(font_name, font_size) #given font name was correct path
        elif os.path.exists(f"{executing_folder}\\{font_name}") and font_name[-4:] == ".ttf":
            if f"{executing_folder}\\{font_name}" not in used_fonts_pathlist: used_fonts_pathlist.append(f"{executing_folder}\\{font_name}")
            return pygame.font.Font(f"{executing_folder}\\{font_name}", font_size) #given font name is font file directly in executing folder, is standard location after basic download and save
        elif os.path.exists(f"{executing_folder}\\{font_name}.ttf"):
            if f"{executing_folder}\\{font_name}.ttf" not in used_fonts_pathlist: used_fonts_pathlist.append(f"{executing_folder}\\{font_name}.ttf")
            return pygame.font.Font(f"{executing_folder}\\{font_name}.ttf", font_size)
        
        #given font name wasn't found in directly in dir executing folder, continue to search sequence
        exec_folder_list = search_file(executing_folder, font_name)[0]
        for path in exec_folder_list:
            if path[-4:] == ".ttf":
                if path.split("\\")[-1] == font_name or path.split("\\")[-1].split(".")[0] == font_name: #exact match
                    if path not in used_fonts_pathlist: used_fonts_pathlist.append(path)
                    return pygame.font.Font(path, font_size)

        for path in exec_folder_list:
            if path[-4:] == ".ttf":
                if path.split("\\")[-1].replace(".ttf","") == font_name:
                    if path not in used_fonts_pathlist: used_fonts_pathlist.append(path)
                    return pygame.font.Font(path, font_size)
        
        windows_font_path = "C\\Windows\\fonts"
        windows_folder_list = search_file(windows_font_path, font_name)[0]
        for path in windows_folder_list:
            if path[-4:] == ".ttf":
                if path.split("\\")[-1] == font_name or path.split("\\")[-1].split(".")[0] == font_name:
                    return pygame.font.Font(path, font_size)
        
        for path in windows_folder_list:
            if path[-4:] == ".ttf":
                if path.split("\\")[-1].replace(".ttf","") == font_name:

                    return pygame.font.Font(path, font_size)
        
        #font name was not found in executing folder and windows font folder or their subdirectories, continue to request of font dict
        if git_token and isinstance(git_token, str):
            font_dict_request = requests.get(f"https://github.com/StijnTB/font_library/raw/main/google_fonts_alphabet_folders/ofl/{font_name[0].capitalize()}/font_links_{font_name[0].capitalize()}.json", headers={"Authorization": f"token {git_token}"})
        else:
            font_dict_request = requests.get(f"https://github.com/StijnTB/font_library/raw/main/google_fonts_alphabet_folders/ofl/{font_name[0].capitalize()}/font_links_{font_name[0].capitalize()}.json")
        
        if font_dict_request.status_code != 200:
            play_logger.warning(f"during http request of font links dictionary, the following status code was recieved: {font_dict_request.status_code}\nusing default font", exc_info=True)
            return pygame.font.Font(pygame.font.get_default_font(), font_size)
        else:
            fonts_dict = font_dict_request.json()
        
        if font_name in fonts_dict or font_name.replace(".ttf", "") in fonts_dict or font_name.lower() in fonts_dict:
            if font_name in fonts_dict: font_file_name = fonts_dict[font_name].split("/")[-1].lower()
            elif font_name.replace(".ttf", "") in fonts_dict: font_file_name = fonts_dict[font_name.replace(".ttf","")].split("/")[-1].lower()
            elif font_name.lower() in fonts_dict: font_file_name = fonts_dict[font_name.lower()].split("/")[-1].lower()
            search_filename_exec_list = search_file(executing_folder, font_file_name)[0]
            for path in search_filename_exec_list:
                if path[-4:] == ".ttf" and path.split("\\")[-1] == font_file_name:
                    return pygame.font.Font(path, font_size)
            
            #font file name wasn't found in executing folder, continue to download sequence
            if git_token and isinstance(git_token, str):
                font_data = requests.get(fonts_dict[font_file_name],headers={"Authorization": f"token {git_token}"})
            else:
                font_data = requests.get(fonts_dict[font_file_name])
            if font_data.status_code != 200:
                play_logger.error(f"during request of font file data, the following status code was recieved: {font_data.status_code}\nusing default font")
                return pygame.font.Font(pygame.font.get_default_font(), font_size)
            else:
                with open(font_file_name, "wb") as new_font_file:
                    new_font_file.write(font_data.content)
                if os.path.isfile(f"{executing_folder}\\{font_file_name}"):
                    return pygame.font.Font(f"{executing_folder}\\{font_file_name}", font_size)
                else:
                    play_logger.warning(f"font file {font_file_name} seems to be saved in a different directory than the executing folder\nusing default font", exc_info=True)
                    return pygame.font.Font(pygame.font.get_default_font(), font_size)
        #font name was not found in fonts dict in any way, use default font
        else:
            if not (font_name.lower() == "none" and font_name == None and font_name.lower == "arial.ttf" and font_name.lower() == "default"): play_logger.warning(f"unable to find font name {font_name} in font list\nusing default font", exc_info=True)
            return pygame.font.Font(pygame.font.get_default_font(), font_size)