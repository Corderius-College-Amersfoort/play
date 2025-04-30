"""This module defines the Circle class, which represents a circle in the game."""

import math as _math
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
        """Create a copy of the circle.
        :return: A copy of the circle."""
        return self.__class__(
            color=self.color,
            radius=self.radius,
            border_color=self.border_color,
            border_width=self.border_width,
            **self._common_properties()
        )

    def update(self):
        """Update the circle's position, size, angle, transparency, and border."""
        if self._should_recompute:
            self.original_image = pygame.Surface(
                (self._radius * 2, self._radius * 2), pygame.SRCALPHA
            )

            if self._border_width > 0:
                pygame.draw.circle(
                    self.original_image,
                    _color_name_to_rgb(self._border_color),
                    (self._radius, self._radius),
                    self._radius,
                )

            pygame.draw.circle(
                self.original_image,
                _color_name_to_rgb(self._color),
                (self._radius, self._radius),
                max(self._radius - self._border_width, 0),
            )

            self.original_image.set_alpha(self._transparency * 2.55)

            self.rect = self.original_image.get_rect()
            pos = convert_pos(self.x, self.y)
            self.rect.x = pos[0] - self._radius
            self.rect.y = pos[1] - self._radius

        if self.physics:
            angle_deg = -_math.degrees(self.physics._pymunk_body.angle)
            self._image = pygame.transform.rotate(self.original_image, angle_deg)
            self.rect = self._image.get_rect(center=self.rect.center)
        else:
            self._image = self.original_image

        super().update()

    ##### color #####
    @property
    def color(self):
        """The color of the circle.
        :return: The color of the circle."""
        return self._color

    @color.setter
    def color(self, _color):
        """Set the color of the circle.
        :param _color: The color of the circle."""
        self._color = _color

    ##### radius #####
    @property
    def radius(self):
        """The radius of the circle.
        :return: The radius of the circle."""
        return self._radius

    @radius.setter
    def radius(self, _radius):
        """Set the radius of the circle.
        :param _radius: The radius of the circle."""
        self._radius = _radius
        if self.physics:
            self.physics._pymunk_shape.unsafe_set_radius(self._radius)

    ##### border_color #####
    @property
    def border_color(self):
        """The color of the circle's border.
        :return: The color of the circle's border."""
        return self._border_color

    @border_color.setter
    def border_color(self, _border_color):
        """Set the color of the circle's border.
        :param _border_color: The color of the circle's border."""
        self._border_color = _border_color

    ##### border_width #####
    @property
    def border_width(self):
        """The width of the circle's border.
        :return: The width of the circle's border."""
        return self._border_width

    @border_width.setter
    def border_width(self, _border_width):
        """Set the width of the circle's border.
        :param _border_width: The width of the circle's border."""
        self._border_width = _border_width
