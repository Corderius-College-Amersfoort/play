"""This module contains the Line class, which is a subclass of Sprite. It is used to create lines in the game window."""

import math as _math

import pygame
from .sprite import Sprite
from ..io.screen import convert_pos, screen
from ..utils import color_name_to_rgb as _color_name_to_rgb


class Line(Sprite):
    def __init__(  # pylint: disable=too-many-arguments
        self,
        color="black",
        x=0,
        y=0,
        length=None,
        angle=None,
        thickness=1,
        x1=None,
        y1=None,
        transparency=100,
        size=100,
    ):
        super().__init__()
        self._x = x
        self._y = y
        self._color = color
        self._thickness = thickness

        # can set either (length, angle) or (x1,y1), otherwise a default is used
        if length is not None and angle is not None:
            self._length = length
            self._angle = angle
            self._x1, self._y1 = self._calc_endpoint()
        elif x1 is not None and y1 is not None:
            self._x1 = x1
            self._y1 = y1
            self._length, self._angle = self._calc_length_angle()
        else:
            # default values
            self._length = length or 100
            self._angle = angle or 0
            self._x1, self._y1 = self._calc_endpoint()

        self._transparency = transparency
        self._size = size

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update()

    def update(self):
        """Update the line's position and appearance."""
        if self._should_recompute:
            pos_begin = convert_pos(self.x, self.y)
            pos_end = convert_pos(self.x1, self.y1)

            self._image = pygame.Surface((screen.width, screen.height), pygame.SRCALPHA)
            pygame.draw.line(
                self._image,
                _color_name_to_rgb(self._color),
                pos_begin,
                pos_end,
                self._thickness,
            )
            self.rect = self._image.get_rect()
            super().update()

    def clone(self):
        """Return a clone of the line.
        :return: A clone of the line."""
        return self.__class__(
            color=self.color,
            length=self.length,
            thickness=self.thickness,
            **self._common_properties()
        )

    ##### color #####
    @property
    def color(self):
        """Return the color of the line.
        :return: The color of the line."""
        return self._color

    @color.setter
    def color(self, _color):
        """Set the color of the line.
        :param _color: The new color of the line."""
        self._color = _color

    ##### thickness #####
    @property
    def thickness(self):
        """Return the thickness of the line.
        :return: The thickness of the line."""
        return self._thickness

    @thickness.setter
    def thickness(self, _thickness):
        """Set the thickness of the line.
        :param _thickness: The new thickness of the line."""
        self._thickness = _thickness

    def _calc_endpoint(self):
        radians = _math.radians(self._angle)
        return (
            self._length * _math.cos(radians) + self.x,
            self._length * _math.sin(radians) + self.y,
        )

    ##### length #####
    @property
    def length(self):
        """Return the length of the line.
        :return: The length of the line
        :rtype: float"""
        return self._length

    @length.setter
    def length(self, _length):
        """Set the length of the line.
        :param _length: The new length of the line."""
        self._length = _length
        self._x1, self._y1 = self._calc_endpoint()

    ##### angle #####
    @property
    def angle(self):
        """Return the angle of the line.
        :return: The angle of the line."""
        return self._angle

    @angle.setter
    def angle(self, _angle):
        """Set the angle of the line.
        :param _angle: The new angle of the line."""
        self._angle = _angle
        self._x1, self._y1 = self._calc_endpoint()
        if self.physics:
            self.physics._pymunk_body.angle = _math.radians(_angle)

    def _calc_length_angle(self):
        dx = self.x1 - self.x
        dy = self.y1 - self.y

        # TODO: this doesn't work at all
        return _math.sqrt(dx**2 + dy**2), _math.degrees(_math.atan2(dy, dx))

    ##### x1 #####
    @property
    def x1(self):
        """Return the x-coordinate of the line's endpoint.
        :return: The x-coordinate of the line's endpoint."""
        return self._x1

    @x1.setter
    def x1(self, _x1):
        """Set the x-coordinate of the line's endpoint.
        :param _x1: The new x-coordinate of the line's endpoint."""
        self._x1 = _x1
        self._length, self._angle = self._calc_length_angle()

    ##### y1 #####
    @property
    def y1(self):
        """Return the y-coordinate of the line's endpoint.
        :return: The y-coordinate of the line's endpoint."""
        return self._y1

    @y1.setter
    def y1(self, _y1):
        """Set the y-coordinate of the line's endpoint.
        :param _y1: The new y-coordinate of the line's endpoint."""
        self._y1 = _y1
        self._length, self._angle = self._calc_length_angle()
