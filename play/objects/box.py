"""This module contains the Box class, which represents a box in the game."""

import math as _math
import pygame
from .sprite import Sprite
from ..io import convert_pos
from ..utils import color_name_to_rgb as _color_name_to_rgb


class Box(Sprite):
    def __init__(
        self,
        color="black",
        x=0,
        y=0,
        width=100,
        height=200,
        border_color="light blue",
        border_width=0,
        border_radius=0,
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
        self._border_radius = border_radius
        self._transparency = transparency
        self._size = size
        self._angle = angle
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update()

    def update(self):
        """Update the box's position, size, angle, transparency, and border."""
        if self._should_recompute:
            self.original_image = pygame.Surface(
                (self._width, self._height), pygame.SRCALPHA
            )

            if self._border_width > 0:
                pygame.draw.rect(
                    self.original_image,
                    _color_name_to_rgb(self._border_color),
                    (0, 0, self._width, self._height),
                    self._border_width,
                    border_radius=self._border_radius,
                )

            pygame.draw.rect(
                self.original_image,
                _color_name_to_rgb(self._color),
                (
                    self._border_width,
                    self._border_width,
                    self._width - 2 * self._border_width,
                    self._height - 2 * self._border_width,
                ),
                border_radius=max(self._border_radius - self._border_width, 0),
            )

            self.original_image.set_alpha(self._transparency * 2.55)
            self.original_image = pygame.transform.rotate(
                self.original_image, self._angle
            )

            self.rect = self.original_image.get_rect()
            pos = convert_pos(self.x, self.y)
            self.rect.x = pos[0] - self._width // 2
            self.rect.y = pos[1] - self._height // 2

        if self.physics:
            angle_deg = -_math.degrees(self.physics._pymunk_body.angle)
            self.image = pygame.transform.rotate(self.original_image, angle_deg)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = self.original_image

        super().update()

    ##### width #####
    @property
    def width(self):
        """The width of the box.
        :return: The width of the box."""
        return self._width

    @width.setter
    def width(self, _width):
        """Set the width of the box.
        :param _width: The new width of the box."""
        self._width = _width

    ##### height #####
    @property
    def height(self):
        """The height of the box.
        :return: The height of the box."""
        return self._height

    @height.setter
    def height(self, _height):
        """Set the height of the box.
        :param _height: The new height of the box."""
        self._height = _height

    ##### color #####
    @property
    def color(self):
        """The color of the box.
        :return: The color of the box."""
        return self._color

    @color.setter
    def color(self, _color):
        """Set the color of the box.
        :param _color: The new color of the box."""
        self._color = _color

    ##### border_color #####
    @property
    def border_color(self):
        """The color of the box's border.
        :return: The color of the box's border."""
        return self._border_color

    @border_color.setter
    def border_color(self, _border_color):
        """Set the color of the box's border.
        :param _border_color: The new color of the box's border."""
        self._border_color = _border_color

    ##### border_width #####
    @property
    def border_width(self):
        """The width of the box's border.
        :return: The width of the box's border."""
        return self._border_width

    @border_width.setter
    def border_width(self, _border_width):
        """Set the width of the box's border.
        :param _border_width: The new width of the box's border."""
        self._border_width = _border_width

    ##### border_radius #####
    @property
    def border_radius(self):
        """The radius of the box's border.
        :return: The radius of the box's border."""
        return self._border_radius

    @border_radius.setter
    def border_radius(self, _border_radius):
        """Set the radius of the box's border.
        :param _border_radius: The new radius of the box's border."""
        self._border_radius = _border_radius

    def clone(self):
        """Create a copy of the box.
        :return: A copy of the box."""
        return self.__class__(
            color=self.color,
            width=self.width,
            height=self.height,
            border_color=self.border_color,
            border_width=self.border_width,
            **self._common_properties()
        )
