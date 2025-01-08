"""This file contains all the IO-related code for the Python Play library."""

from sys import platform

import pygame
from screeninfo import get_monitors
import pymunk as _pymunk
from pygame._sdl2.video import Window  # pylint: disable=no-name-in-module
from pygame.locals import *

from ..globals import globals_list
from ..physics import physics_space

PYGAME_DISPLAY = None


class Screen:
    def __init__(self, width=globals_list.WIDTH, height=globals_list.HEIGHT):
        global PYGAME_DISPLAY

        self._width = width
        self._height = height
        PYGAME_DISPLAY = pygame.display.set_mode(
            (width, height), pygame.DOUBLEBUF  # pylint: disable=no-member
        )  # pylint: disable=no-member
        pygame.display.set_caption("Python Play")
        self._fullscreen = False

    @property
    def width(self):
        """Get the width of the screen.
        :return: The width of the screen."""
        return self._width

    @width.setter
    def width(self, _width):
        """Set the width of the screen.
        :param _width: The new width of the screen."""
        global PYGAME_DISPLAY
        self._width = _width

        remove_walls()
        create_walls()

        if self._fullscreen:
            self.enable_fullscreen()
        else:
            PYGAME_DISPLAY = pygame.display.set_mode((self._width, self._height))

    @property
    def height(self):
        """Get the height of the screen.
        :return: The height of the screen."""
        return self._height

    @height.setter
    def height(self, _height):
        """Set the height of the screen.
        :param _height: The new height of the screen."""
        global PYGAME_DISPLAY
        self._height = _height

        remove_walls()
        create_walls()

        if self._fullscreen:
            self.enable_fullscreen()
        else:
            PYGAME_DISPLAY = pygame.display.set_mode((self._width, self._height))

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

    def enable_fullscreen(self):
        """Enable fullscreen mode."""
        global PYGAME_DISPLAY
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
            PYGAME_DISPLAY = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
            window = Window.from_display_module()
            window.position = (0, 0)
        else:
            PYGAME_DISPLAY = pygame.display.set_mode(
                (width, height),
                SCALED + NOFRAME + FULLSCREEN,  # pylint: disable=undefined-variable
                32,  # pylint: disable=undefined-variable
            )

    def disable_fullscreen(self):
        """Disable fullscreen mode."""
        global PYGAME_DISPLAY
        if not self._fullscreen:
            return
        self._fullscreen = False
        pygame.display.quit()
        pygame.display.init()
        PYGAME_DISPLAY = pygame.display.set_mode((self.width, self.height))


screen = Screen()


def _create_wall(a, b):
    segment = _pymunk.Segment(physics_space.static_body, a, b, 0.0)
    segment.elasticity = 1.0
    segment.friction = 0.1
    physics_space.add(segment)
    return segment


def create_walls():
    """Create walls around the screen."""
    globals_list.walls.append(
        _create_wall([screen.left, screen.top], [screen.right, screen.top])
    )  # top
    globals_list.walls.append(
        _create_wall([screen.left, screen.bottom], [screen.right, screen.bottom])
    )  # bottom
    globals_list.walls.append(
        _create_wall([screen.left, screen.bottom], [screen.left, screen.top])
    )  # left
    globals_list.walls.append(
        _create_wall([screen.right, screen.bottom], [screen.right, screen.top])
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
