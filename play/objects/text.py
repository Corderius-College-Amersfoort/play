"""This module contains the Text class, which is used to create text objects in the game."""

import pygame
from .sprite import Sprite
from ..io import convert_pos
from ..utils import color_name_to_rgb as _color_name_to_rgb


class Text(Sprite):
    def __init__(  # pylint: disable=too-many-arguments
        self,
        words="hi :)",
        x=0,
        y=0,
        font=None,
        font_size=50,
        color="black",
        angle=0,
        transparency=100,
        size=100,
    ):
        super().__init__()
        self._font = font
        self._font_size = font_size
        self._pygame_font = pygame.font.Font(font, font_size)
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
        """Get the words of the text object.
        :return: The words of the text object."""
        return self._words

    @words.setter
    def words(self, string):
        """Set the words of the text object.
        :param string: The new words of the text object."""
        self._words = str(string)

    @property
    def font(self):
        """Get the font of the text object.
        :return: The font of the text object."""
        return self._font

    @font.setter
    def font(self, font_name):
        """Set the font of the text object.
        :param font_name: The new font of the text object."""
        self._font = str(font_name)

    @property
    def font_size(self):
        """Get the font size of the text object.
        :return: The font size of the text object."""
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        self._font_size = size

    @property
    def color(self):
        """Get the color of the text object.
        :return: The color of the text object."""
        return self._color

    @color.setter
    def color(self, color_):
        self._color = color_
