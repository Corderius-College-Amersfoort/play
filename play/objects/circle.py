import pygame
from .sprite import Sprite
from ..all_sprites import all_sprites
from ..color import color_name_to_rgb as _color_name_to_rgb


class Circle(Sprite):
    def __init__(self, color='black', x=0, y=0, radius=100, border_color='light blue', border_width=0, transparency=100,
                 size=100, angle=0):
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

        self._compute_primary_surface()

        all_sprites.append(self)

    def clone(self):
        return self.__class__(color=self.color, radius=self.radius, border_color=self.border_color,
                              border_width=self.border_width, **self._common_properties())

    def _compute_primary_surface(self):
        total_diameter = (self.radius + self._border_width) * 2
        self._primary_pygame_surface = pygame.Surface((total_diameter, total_diameter), pygame.SRCALPHA)

        center = self._radius + self._border_width

        if self._border_width and self._border_color:
            # draw border circle
            pygame.draw.circle(self._primary_pygame_surface, _color_name_to_rgb(self._border_color), (center, center),
                               self._radius)
            # draw fill circle over border circle
            pygame.draw.circle(self._primary_pygame_surface, _color_name_to_rgb(self._color), (center, center),
                               self._radius - self._border_width)
        else:
            pygame.draw.circle(self._primary_pygame_surface, _color_name_to_rgb(self._color), (center, center),
                               self._radius)

        self._should_recompute_primary_surface = False
        self._compute_secondary_surface(force=True)

    ##### color #####
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, _color):
        self._color = _color
        self._should_recompute_primary_surface = True

    ##### radius #####
    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, _radius):
        self._radius = _radius
        self._should_recompute_primary_surface = True
        if self.physics:
            self.physics._pymunk_shape.unsafe_set_radius(self._radius)

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


def new_circle(color='black', x=0, y=0, radius=100, border_color='light blue', border_width=0, transparency=100,
               size=100, angle=0):
    return Circle(color=color, x=x, y=y, radius=radius, border_color=border_color, border_width=border_width,
                  transparency=transparency, size=size, angle=angle)
