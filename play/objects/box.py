"""This module contains the Box class, which represents a box in the game."""

import pygame
from .sprite import Sprite
from ..all_sprites import all_sprites
from ..color import color_name_to_rgb as _color_name_to_rgb


class Box(Sprite):
    def __init__( # pylint: disable=too-many-arguments
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
        super().__init__(x, y, size, angle, transparency)
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color = color
        self._border_color = border_color
        self._border_width = border_width

        self._transparency = transparency
        self._size = size
        self._angle = angle
        self._is_clicked = False
        self._is_hidden = False
        self.physics = None

        self._when_clicked_callbacks = []

        self._compute_primary_surface()

        all_sprites.append(self)

    def _compute_primary_surface(self):
        self._primary_pygame_surface = pygame.Surface(
            (self._width, self._height), pygame.SRCALPHA # pylint: disable=no-member
        )

        if self._border_width and self._border_color:
            # draw border rectangle
            self._primary_pygame_surface.fill(_color_name_to_rgb(self._border_color))
            # draw fill rectangle over border rectangle at the proper position
            pygame.draw.rect(
                self._primary_pygame_surface,
                _color_name_to_rgb(self._color),
                (
                    self._border_width,
                    self._border_width,
                    self._width - 2 * self._border_width,
                    self._height - 2 * self.border_width,
                ),
            )

        else:
            self._primary_pygame_surface.fill(_color_name_to_rgb(self._color))

        self._should_recompute_primary_surface = False
        self._compute_secondary_surface(force=True)

    ##### width #####
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, _width):
        self._width = _width
        self._should_recompute_primary_surface = True

    ##### height #####
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, _height):
        self._height = _height
        self._should_recompute_primary_surface = True

    ##### color #####
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, _color):
        self._color = _color
        self._should_recompute_primary_surface = True

    ##### border_color #####
    @property
    def border_color(self):
        return self._border_color

    @border_color.setter
    def border_color(self, _border_color):
        self._border_color = _border_color
        self._should_recompute_primary_surface = True

    ##### border_width #####
    @property
    def border_width(self):
        return self._border_width

    @border_width.setter
    def border_width(self, _border_width):
        self._border_width = _border_width
        self._should_recompute_primary_surface = True

    def clone(self):
        return self.__class__(
            color=self.color,
            width=self.width,
            height=self.height,
            border_color=self.border_color,
            border_width=self.border_width,
            **self._common_properties()
        )


def new_box( # pylint: disable=too-many-arguments
    color="black",
    x=0,
    y=0,
    width=100,
    height=200,
    border_color="light blue",
    border_width=0,
    angle=0,
    transparency=100,
    size=100,
):
    return Box(
        color=color,
        x=x,
        y=y,
        width=width,
        height=height,
        border_color=border_color,
        border_width=border_width,
        angle=angle,
        transparency=transparency,
        size=size,
    )
