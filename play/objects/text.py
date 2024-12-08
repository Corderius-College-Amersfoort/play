"""This module contains the Text class, which is a text string in the game."""

import os
import pygame
from .sprite import Sprite
from ..io import convert_pos
from ..utils import color_name_to_rgb as _color_name_to_rgb
from ..io.logging import play_logger


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
    ):
        super().__init__()
        self._font = font
        self._font_size = font_size
        self._pygame_font = self._load_font(font, font_size)
        self._words = words
        self._color = color

        self._x = x
        self._y = y

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
    def font(self):
        """Get the font of the text object."""
        return self._font

    @font.setter
    def font(self, font_name):
        """Set the font of the text object. This will load the font dynamically."""
        self._font = font_name
        self._pygame_font = self._load_font(font_name, self._font_size)

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

    def _load_font(self, font_name, font_size):
        """Helper method to load a font, either from a file or system."""
        if font_name == "default":
            return pygame.font.Font(pygame.font.get_default_font(), font_size)

        if os.path.isfile(font_name):
            return pygame.font.Font(font_name, font_size)
        play_logger.warning(
            "File to font doesnt exist, Using default font", exc_info=True
        )
        return pygame.font.Font(pygame.font.get_default_font(), font_size)
