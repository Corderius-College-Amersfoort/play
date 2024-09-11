"""This module contains the Box class, which represents a box in the game."""

import pygame
from .sprite import Sprite
from ..globals import all_sprites
from ..io import convert_pos
from ..utils import color_name_to_rgb as _color_name_to_rgb


class Box(Sprite):
    def __init__(  # pylint: disable=too-many-arguments
        self,
        color="black",
        x=0,
        y=0,
        width=100,
        height=200,
        border_color="light blue",
        border_width=0,
        transparency=100,
        size=100,
        angle=0,
    ):
        super().__init__(self)
        self._color = color
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._border_color = border_color
        self._border_width = border_width
        self._transparency = transparency
        self._size = size
        self._angle = angle
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update()

    def update(self):
        self.image = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        self.image.fill(_color_name_to_rgb(self._color))
        self.image.set_alpha(self._transparency)
        self.rect = self.image.get_rect()
        pos = convert_pos(self.x, self.y)
        self.rect.x = pos[0] - self._width // 2
        self.rect.y = pos[1] - self._height // 2

    ##### width #####
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, _width):
        self._width = _width
        self._should_recompute = True

    ##### height #####
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, _height):
        self._height = _height
        self._should_recompute = True

    ##### color #####
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, _color):
        self._color = _color
        self._should_recompute = True

    ##### border_color #####
    @property
    def border_color(self):
        return self._border_color

    @border_color.setter
    def border_color(self, _border_color):
        self._border_color = _border_color
        self._should_recompute = True

    ##### border_width #####
    @property
    def border_width(self):
        return self._border_width

    @border_width.setter
    def border_width(self, _border_width):
        self._border_width = _border_width
        self._should_recompute = True

    def clone(self):
        return self.__class__(
            color=self.color,
            width=self.width,
            height=self.height,
            border_color=self.border_color,
            border_width=self.border_width,
            **self._common_properties()
        )
