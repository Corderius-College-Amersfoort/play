"""This module provides a wrapper around the Pygame display module to create a screen object"""

from sys import platform

import pygame
from pygame import (  # pylint: disable=no-name-in-module
    Window,
    SCALED,
    NOFRAME,
    FULLSCREEN,
)
from screeninfo import get_monitors

import pymunk as _pymunk

from ..callback import run_callback, CallbackType, callback_manager
from ..globals import globals_list
from ..physics import physics_space
from ..utils.async_helpers import make_async

PYGAME_DISPLAY = None


class Screen:
    def update_display(self, extra_flags=0):
        """Update the display with the current width and height."""
        globals_list.display = pygame.display.set_mode(
            (self._width, self._height),
            (
                pygame.RESIZABLE
                if self._resizable
                else 0 | pygame.DOUBLEBUF | extra_flags
            ),  # pylint: disable=no-member
        )  # pylint: disable=no-member

    def __init__(self, width=globals_list.WIDTH, height=globals_list.HEIGHT):
        self._width = width
        self._height = height

        self._resizable = False
        self._fullscreen = False
        self._caption = "Python Play"

        self.update_display()
        pygame.display.set_caption(self._caption)

    @property
    def caption(self):
        """Get the caption of the screen.
        :return: The caption of the screen."""
        return self._caption

    @caption.setter
    def caption(self, _caption):
        """Set the caption of the screen.
        :param _caption: The new caption of the screen."""
        self._caption = _caption
        pygame.display.set_caption(self._caption)

    @property
    def resizable(self):
        """Get whether the screen is resizable.
        :return: Whether the screen is resizable."""
        return self._resizable

    @resizable.setter
    def resizable(self, _resizable):
        """Set whether the screen is resizable.
        :param _resizable: Whether the screen is resizable."""
        self._resizable = _resizable

    @property
    def width(self):
        """Get the width of the screen.
        :return: The width of the screen."""
        return self._width

    @width.setter
    def width(self, _width):
        """Set the width of the screen.
        :param _width: The new width of the screen."""
        self._width = _width

        remove_walls()
        create_walls()

        if self._fullscreen:
            self.enable_fullscreen()

    @property
    def height(self):
        """Get the height of the screen.
        :return: The height of the screen."""
        return self._height

    @height.setter
    def height(self, _height):
        """Set the height of the screen.
        :param _height: The new height of the screen."""
        self._height = _height

        remove_walls()
        create_walls()

        if self._fullscreen:
            self.enable_fullscreen()

    @property
    def top(self):
        """Get the top side of the screen.
        :return: The top side of the screen."""
        return self.height / 2

    @property
    def bottom(self):
        """Get the bottom side of the screen.
        :return: The bottom side of the screen."""
        return self.height / -2

    @property
    def left(self):
        """Get the left side of the screen.
        :return: The left side of the screen."""
        return self.width / -2

    @property
    def right(self):
        """Get the right side of the screen.
        :return: The right side of the screen."""
        return self.width / 2

    @property
    def size(self):
        """Get the size of the screen.
        :return: The size of the screen."""
        return self.width, self.height

    def when_resized(self, func):
        """Run a function when the screen is resized.
        :param func: The function to run."""
        async_callback = make_async(func)

        async def wrapper():
            run_callback(
                async_callback,
                [],
                [],
            )

        callback_manager.add_callback(
            CallbackType.WHEN_RESIZED,
            wrapper,
        )
        return wrapper

    def enable_fullscreen(self):
        """Enable fullscreen mode."""
        if self._fullscreen:
            return
        self._fullscreen = True

        width = get_monitors()[0].width
        height = get_monitors()[0].height

        self._width = width
        self._height = height

        remove_walls()
        create_walls()

        if platform != "linux":
            self.update_display(pygame.FULLSCREEN)
            window = Window.from_display_module()
            window.position = (0, 0)
        else:
            self.update_display(
                SCALED + NOFRAME + FULLSCREEN,
            )

    def disable_fullscreen(self):
        """Disable fullscreen mode."""
        if not self._fullscreen:
            return
        self._fullscreen = False
        pygame.display.quit()
        pygame.display.init()
        self.update_display()


screen = Screen()


def create_wall(a, b):
    """Create a wall segment in the physics space.
    :param a: The start point of the wall segment.
    :param b: The end point of the wall segment."""
    segment = _pymunk.Segment(physics_space.static_body, a, b, 0.0)
    segment.elasticity = 1.0
    segment.friction = 0.0
    physics_space.add(segment)
    return segment


def create_walls():
    """Create walls around the screen."""
    globals_list.walls.append(
        create_wall([screen.left, screen.top], [screen.right, screen.top])
    )  # top
    globals_list.walls.append(
        create_wall([screen.left, screen.bottom], [screen.right, screen.bottom])
    )  # bottom
    globals_list.walls.append(
        create_wall([screen.left, screen.bottom], [screen.left, screen.top])
    )  # left
    globals_list.walls.append(
        create_wall([screen.right, screen.bottom], [screen.right, screen.top])
    )  # right


def remove_walls():
    """Remove the walls from the physics space."""
    for wall in globals_list.walls:
        physics_space.remove(wall)
    globals_list.walls.clear()


def remove_wall(index):
    """Remove a wall from the physics space.
    :param index: The index of the wall to remove. 0: top, 1: bottom, 2: left, 3: right.
    """
    physics_space.remove(globals_list.walls[index])
    globals_list.walls.pop(index)


create_walls()


def convert_pos(x, y):
    """
    Convert from the Play coordinate system to the Pygame coordinate system.
    :param x: The x-coordinate in the Play coordinate system.
    :param y: The y-coordinate in the Play coordinate system.
    """
    x1 = screen.width / 2 + x
    y1 = screen.height / 2 - y
    return x1, y1


def pos_convert(x, y):
    """
    Convert from the Pygame coordinate system to the Play coordinate system.
    :param x: The x-coordinate in the Pygame coordinate system.
    :param y: The y-coordinate in the Pygame coordinate system.
    """
    x1 = x - screen.width / 2
    y1 = screen.height / 2 - y
    return x1, y1
