import pygame
from ..all_sprites import _walls
from ..physics import physics_space
import pymunk as _pymunk


class Screen(object):
    def __init__(self, width=800, height=600):
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, _width):
        self._width = _width

        remove_walls()
        create_walls()

        pygame.display.set_mode((self._width, self._height))

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, _height):
        self._height = _height

        remove_walls()
        create_walls()

        pygame.display.set_mode((self._width, self._height))

    @property
    def top(self):
        return self.height / 2

    @property
    def bottom(self):
        return self.height / -2

    @property
    def left(self):
        return self.width / -2

    @property
    def right(self):
        return self.width / 2


screen = Screen()


def _create_wall(a, b):
    segment = _pymunk.Segment(physics_space.static_body, a, b, 0.0)
    segment.elasticity = 1.0
    segment.friction = .1
    physics_space.add(segment)
    return segment


def create_walls():
    _walls.append(_create_wall([screen.left, screen.top], [screen.right, screen.top]))  # top
    _walls.append(_create_wall([screen.left, screen.bottom], [screen.right, screen.bottom]))  # bottom
    _walls.append(_create_wall([screen.left, screen.bottom], [screen.left, screen.top]))  # left
    _walls.append(_create_wall([screen.right, screen.bottom], [screen.right, screen.top]))  # right


def remove_walls():
    physics_space.remove(_walls)
    _walls.clear()


create_walls()
