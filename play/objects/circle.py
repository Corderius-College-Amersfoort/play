"""This module defines the Circle class, which represents a circle in the game."""

import pygame
from .sprite import Sprite
from ..io import convert_pos
from ..utils import color_name_to_rgb as _color_name_to_rgb


class Circle(Sprite):
    def __init__(
        self,
        color="black",
        x=0,
        y=0,
        radius=100,
        border_color="light blue",
        border_width=0,
        transparency=100,
        size=100,
        angle=0,
    ):
        super().__init__()
        self._x = x
        self._y = y
        self._color = color
        self._radius = radius
        self._border_color = border_color
        self._border_width = border_width

        self._transparency = transparency
        self._size = size
        self._angle = angle
        self._is_clicked = False
        self._is_hidden = False
        self.physics = None

        self._when_clicked_callbacks = []

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update()

    def clone(self):
        return self.__class__(
            color=self.color,
            radius=self.radius,
            border_color=self.border_color,
            border_width=self.border_width,
            **self._common_properties()
        )

    def update(self):
        self._image = pygame.Surface(
            (self._radius * 2, self._radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self._image,
            _color_name_to_rgb(self._color),
            (self._radius, self._radius),
            self._radius,
        )
        self.rect = self._image.get_rect()
        pos = convert_pos(self.x, self.y)
        self.rect.x = pos[0] - self._radius
        self.rect.y = pos[1] - self._radius
        # self._should_recompute = False

    ##### color #####
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, _color):
        self._color = _color
        self._should_recompute = True

    ##### radius #####
    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, _radius):
        self._radius = _radius
        self._should_recompute = True
        if self.physics:
            self.physics._pymunk_shape.unsafe_set_radius(self._radius)

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
