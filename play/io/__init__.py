import pygame
from ..all_sprites import _walls
from ..physics import physics_space
import pymunk as _pymunk
from pygame._sdl2.video import Window
from pygame.locals import *
from sys import platform

_pygame_display = None

class Screen(object):
    def __init__(self, width=800, height=600):
        global _pygame_display
        self._width = width
        self._height = height
        _pygame_display = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
        pygame.display.set_caption("Python Play")
        self._fullscreen = False

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, _width):
        global _pygame_display
        self._width = _width

        remove_walls()
        create_walls()

        if self._fullscreen:
            self.enable_fullscreen()
        else:
            _pygame_display = pygame.display.set_mode((self._width, self._height))

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, _height):
        global _pygame_display
        self._height = _height

        remove_walls()
        create_walls()

        if self._fullscreen:
            self.enable_fullscreen()
        else:
            _pygame_display = pygame.display.set_mode((self._width, self._height))

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

    @property
    def size(self):
        return self.width, self.height

    def enable_fullscreen(self):
        global _pygame_display
        if self._fullscreen:
            return
        self._fullscreen = True
        window = Window.from_display_module()
        full_screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        if platform != 'linux':
            pygame.display.toggle_fullscreen()  # works for entering and exiting fullscreen, except in linux
            window.position = (full_screen_size[i] / 2 - window.size[i] / 2 for i in
                               range(2))  # reset X and Y position of the window to original instead of top left
        else:
            _pygame_display = pygame.display.set_mode((self.width, self.height), SCALED + NOFRAME + FULLSCREEN, 32)  # all flags are necessary

    def disable_fullscreen(self):
        global _pygame_display
        if not self._fullscreen:
            return
        self._fullscreen = False
        pygame.display.quit()
        pygame.display.init()
        _pygame_display = pygame.display.set_mode((self.width, self.height))


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
