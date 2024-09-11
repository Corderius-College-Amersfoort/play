"""This module contains the base sprite class for all objects in the game."""

import math as _math
import warnings as _warnings
import pymunk as _pymunk
import pygame

from ..globals import all_sprites, sprites_group
from ..io.exceptions import Oops, Hmm
from ..physics import physics_space, _Physics
from ..utils import _clamp
from ..io import screen
from ..utils.async_helpers import _make_async


def _circle_touching_circle(a, b):
    # determine which is the circle and which is the sprite or if they're both circles
    if hasattr(a, "_radius") and hasattr(b, "_radius"):
        return a.distance_to(b) <= a.radius + b.radius
    elif hasattr(a, "_radius"):
        return a.distance_to(b) <= a.radius
    return b.distance_to(a) <= b.radius


def _sprite_touching_sprite(a, b):
    return pygame.sprite.collide_mask(a, b) is not None


def point_touching_sprite(point, sprite):
    # todo: custom code for circle, line, rotated rectangley sprites
    return (
        sprite.left <= point.x <= sprite.right
        and sprite.bottom <= point.y <= sprite.top
    )


class Sprite(
    pygame.sprite.Sprite
):  # pylint: disable=attribute-defined-outside-init, too-many-public-methods
    def __init__(self, image=None):
        self._size = None
        self._x = None
        self._y = None
        self._angle = None
        self._transparency = None

        self._should_recompute = False
        self._image = image
        self.physics = None
        self._is_clicked = False
        self._is_hidden = False

        self._when_clicked_callbacks = []

        pygame.sprite.Sprite.__init__(self)
        sprites_group.add(self)

    @property
    def is_clicked(self):
        return self._is_clicked

    def move(self, steps=3):
        angle = _math.radians(self.angle)
        self.x += steps * _math.cos(angle)
        self.y += steps * _math.sin(angle)

    def turn(self, degrees=10):
        self.angle += degrees

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, _x):
        prev_x = self._x
        self._x = _x
        if self.physics:
            self.physics._pymunk_body.position = self._x, self._y
            if prev_x != _x:
                # setting velocity makes the simulation more realistic usually
                self.physics._pymunk_body.velocity = (
                    _x - prev_x,
                    self.physics._pymunk_body.velocity.y,
                )
            if self.physics._pymunk_body.body_type == _pymunk.Body.STATIC:
                physics_space.reindex_static()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, _y):
        prev_y = self._y
        self._y = _y
        if self.physics:
            self.physics._pymunk_body.position = self._x, self._y
            if prev_y != _y:
                # setting velocity makes the simulation more realistic usually
                self.physics._pymunk_body.velocity = (
                    self.physics._pymunk_body.velocity.x,
                    _y - prev_y,
                )
            if self.physics._pymunk_body.body_type == _pymunk.Body.STATIC:
                physics_space.reindex_static()

    @property
    def transparency(self):
        return self._transparency

    @transparency.setter
    def transparency(self, alpha):
        if not isinstance(alpha, float) and not isinstance(alpha, int):
            raise Oops(
                f"""Looks like you're trying to set {self}'s transparency to '{alpha}', which isn't a number.
Try looking in your code for where you're setting transparency for {self} and change it a number.
"""
            )
        if alpha > 100 or alpha < 0:
            _warnings.warn(
                f"""The transparency setting for {self} is being set to {alpha} and it should be between 0 and 100.
You might want to look in your code where you're setting transparency and make sure it's between 0 and 100.  """,
                Hmm,
            )

        self._transparency = _clamp(alpha, 0, 100)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image_filename):
        self._image = image_filename
        self._should_recompute = True

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, _angle):
        self._angle = _angle

        if self.physics:
            self.physics._pymunk_body.angle = _math.radians(_angle)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, percent):
        self._size = percent
        if self.physics:
            self.physics._remove()
            self.physics._make_pymunk()

    def hide(self):
        self._is_hidden = True
        if self.physics:
            self.physics.pause()

    def show(self):
        self._is_hidden = False
        if self.physics:
            self.physics.unpause()

    @property
    def is_hidden(self):
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, hide):
        self._is_hidden = hide

    @property
    def is_shown(self):
        return not self._is_hidden

    @is_shown.setter
    def is_shown(self, show):
        self._is_hidden = not show

    def is_touching(self, sprite_or_point):
        if isinstance(sprite_or_point, Sprite):
            return _sprite_touching_sprite(sprite_or_point, self)
        return point_touching_sprite(sprite_or_point, self)

    def point_towards(self, x, y=None):
        try:
            x, y = x.x, x.y
        except AttributeError:
            pass
        self.angle = _math.degrees(_math.atan2(y - self.y, x - self.x))

    def go_to(self, x=None, y=None):
        """
        Example:

            # text will follow around the mouse
            text = play.new_text('yay')

            @play.repeat_forever
            async def do():
                text.go_to(play.mouse)
        """
        assert not x is None

        try:
            # users can call e.g. sprite.go_to(play.mouse), so x will be an object with x and y
            self.x = x.x
            self.y = x.y
        except AttributeError:
            self.x = x
            self.y = y

    def distance_to(self, x, y=None):
        assert not x is None

        try:
            # x can either be a number or a sprite. If it's a sprite:
            x1 = x.x
            y1 = x.y
        except AttributeError:
            x1 = x
            y1 = y

        dx = self.x - x1
        dy = self.y - y1

        return _math.sqrt(dx**2 + dy**2)

    def remove(self):
        if self.physics:
            self.physics._remove()
        sprites_group.remove(self)

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    @property
    def right(self):
        return self.x + self.width / 2

    @right.setter
    def right(self, x):
        self.x = x - self.width / 2

    @property
    def left(self):
        return self.x - self.width / 2

    @left.setter
    def left(self, x):
        self.x = x + self.width / 2

    @property
    def top(self):
        return self.y + self.height / 2

    @top.setter
    def top(self, y):
        self.y = y - self.height / 2

    @property
    def bottom(self):
        return self.y - self.height / 2

    @bottom.setter
    def bottom(self, y):
        self.y = y + self.height / 2

    def _pygame_x(self):
        return self.x + (screen.width / 2.0) - (self.rect.width / 2.0)

    def _pygame_y(self):
        return (screen.height / 2.0) - self.y - (self.rect.height / 2.0)

    # @decorator
    def when_clicked(self, callback, call_with_sprite=False):
        async_callback = _make_async(callback)

        async def wrapper():
            wrapper.is_running = True
            if call_with_sprite:
                await async_callback(self)
            else:
                await async_callback()
            wrapper.is_running = False

        wrapper.is_running = False
        self._when_clicked_callbacks.append(wrapper)
        return wrapper

    def _common_properties(self):
        # used with inheritance to clone
        return {
            "x": self.x,
            "y": self.y,
            "size": self.size,
            "transparency": self.transparency,
            "angle": self.angle,
        }

    def clone(self):
        # TODO: make work with physics
        return self.__class__(image=self.image, **self._common_properties())

    # def __getattr__(self, key):
    #     # TODO: use physics as a proxy object so users can do e.g. sprite.x_speed
    #     if not self.physics:
    #         return getattr(self, key)
    #     else:
    #         return getattr(self.physics, key)

    # def __setattr__(self, name, value):
    #     if not self.physics:
    #         return setattr(self, name, value)
    #     elif self.physics and name in :
    #         return setattr(self.physics, name, value)

    def start_physics(  # pylint: disable=too-many-arguments
        self,
        can_move=True,
        stable=False,
        x_speed=0,
        y_speed=0,
        obeys_gravity=True,
        bounciness=1.0,
        mass=10,
        friction=0.1,
    ):
        if not self.physics:
            self.physics = _Physics(
                self,
                can_move,
                stable,
                x_speed,
                y_speed,
                obeys_gravity,
                bounciness,
                mass,
                friction,
            )

    def stop_physics(self):
        self.physics._remove()
        self.physics = None
