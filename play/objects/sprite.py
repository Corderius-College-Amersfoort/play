"""This module contains the base sprite class for all objects in the game."""

import math as _math
import warnings as _warnings
import pymunk as _pymunk
import pygame

from ..loop import loop as _loop
from ..globals import sprites_group
from ..physics import physics_space, Physics as _Physics
from ..utils import _clamp
from ..io import screen
from ..utils.async_helpers import _make_async


def _sprite_touching_sprite(a, b):
    """Check if two sprites are touching.
    :param a: The first sprite to check if it's touching the other sprite.
    :param b: The second sprite to check if it's touching the other sprite.
    :return: Whether the two sprites are touching."""
    return a.rect.colliderect(b.rect)


def point_touching_sprite(point, sprite):
    """Check if a point is touching a sprite.
    :param point: The point to check if it's touching the sprite.
    :param sprite: The sprite to check if it's touching the point.
    :return: Whether the point is touching the sprite."""
    return sprite.rect.collidepoint(point)


_should_ignore_update = ["_should_recompute", "rect", "_image", "image"]


class Sprite(
    pygame.sprite.Sprite
):  # pylint: disable=attribute-defined-outside-init, too-many-public-methods
    def __init__(self, image=None):
        self._size = None
        self._x = None
        self._y = None
        self._angle = None
        self._transparency = None

        self._when_touching_callbacks = []
        self._dependent_sprites = []
        self._active_callbacks = []

        self._image = image
        self.physics = None
        self._is_clicked = False
        self._is_hidden = False
        self._should_recompute = True

        self._when_clicked_callbacks = []

        self.rect = None

        super().__init__()
        sprites_group.add(self)

    def __setattr__(self, name, value):
        # ignore if it's in the ignored list or if the variable doesn't change
        if name not in _should_ignore_update and getattr(self, name, value) != value:
            self._should_recompute = True
            for sprite in self._dependent_sprites:
                sprite._should_recompute = True
        super().__setattr__(name, value)

    def update(self):
        """Update the sprite."""
        if self._should_recompute and self._when_touching_callbacks:
            # check if we are touching any other sprites
            for callback, b in self._when_touching_callbacks:
                if self.is_touching(b):
                    if callback not in self._active_callbacks:
                        self._active_callbacks.append(callback)
                else:
                    if callback in self._active_callbacks:
                        self._active_callbacks.remove(callback)
            self._should_recompute = False

    @property
    def is_clicked(self):
        """Get whether the sprite is clicked.
        :return: Whether the sprite is clicked."""
        return self._is_clicked

    def move(self, steps=3):
        """Move the sprite.
        :param steps: The number of steps to move the sprite."""
        angle = _math.radians(self.angle)
        self.x += steps * _math.cos(angle)
        self.y += steps * _math.sin(angle)

    def turn(self, degrees=10):
        """Turn the sprite.
        :param degrees: The number of degrees to turn the sprite."""
        self.angle += degrees

    @property
    def x(self):
        """Get the x-coordinate of the sprite.
        :return: The x-coordinate of the sprite."""
        return self._x

    @x.setter
    def x(self, _x):
        """Set the x-coordinate of the sprite.
        :param _x: The x-coordinate of the sprite."""
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
        """Get the y-coordinate of the sprite.
        :return: The y-coordinate of the sprite."""
        return self._y

    @y.setter
    def y(self, _y):
        """Set the y-coordinate of the sprite.
        :param _y: The y-coordinate of the sprite."""
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
        """Get the transparency of the sprite.
        :return: The transparency of the sprite."""
        return self._transparency

    @transparency.setter
    def transparency(self, alpha):
        """Set the transparency of the sprite.
        :param alpha: The transparency of the sprite."""
        if not isinstance(alpha, float) and not isinstance(alpha, int):
            raise ValueError(
                f"""Looks like you're trying to set {self}'s transparency to '{alpha}', which isn't a number.
Try looking in your code for where you're setting transparency for {self} and change it a number.
"""
            )
        if alpha > 100 or alpha < 0:
            _warnings.warn(
                f"""The transparency setting for {self} is being set to {alpha} and it should be between 0 and 100.
You might want to look in your code where you're setting transparency and make sure it's between 0 and 100.  """,
                Warning,
            )

        self._transparency = _clamp(alpha, 0, 100)

    @property
    def image(self):
        """Get the image of the sprite.
        :return: The image of the sprite."""
        return self._image

    @image.setter
    def image(self, image_filename):
        """Set the image of the sprite.
        :param image_filename: The filename of the image to set."""
        self._image = image_filename

    @property
    def angle(self):
        """Get the angle of the sprite.
        :return: The angle of the sprite."""
        return self._angle

    @angle.setter
    def angle(self, _angle):
        """Set the angle of the sprite.
        :param _angle: The angle of the sprite."""
        self._angle = _angle

        if self.physics:
            self.physics._pymunk_body.angle = _math.radians(_angle)

    @property
    def size(self):
        """Get the size of the sprite.
        :return: The size of the sprite."""
        return self._size

    @size.setter
    def size(self, percent):
        """Set the size of the sprite.
        :param percent: The size of the sprite as a percentage."""
        self._size = percent
        if self.physics:
            self.physics._remove()
            self.physics._make_pymunk()

    def hide(self):
        """Hide the sprite."""
        self._is_hidden = True
        if self.physics:
            self.physics.pause()

    def show(self):
        """Show the sprite."""
        self._is_hidden = False
        if self.physics:
            self.physics.unpause()

    @property
    def is_hidden(self):
        """Get whether the sprite is hidden.
        :return: Whether the sprite is hidden."""
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, hide):
        """Set whether the sprite is hidden.
        :param hide: Whether the sprite is hidden."""
        self._is_hidden = hide

    @property
    def is_shown(self):
        """Get whether the sprite is shown.
        :return: Whether the sprite is shown."""
        return not self._is_hidden

    @is_shown.setter
    def is_shown(self, show):
        """Set whether the sprite is shown.
        :param show: Whether the sprite is shown."""
        self._is_hidden = not show

    def is_touching(self, sprite_or_point):
        """Check if the sprite is touching another sprite or a point.
        :param sprite_or_point: The sprite or point to check if it's touching.
        :return: Whether the sprite is touching the other sprite or point."""
        if isinstance(sprite_or_point, Sprite):
            return _sprite_touching_sprite(self, sprite_or_point)
        return point_touching_sprite(sprite_or_point, self)

    def point_towards(self, x, y=None):
        """Point the sprite towards a point or another sprite.
        :param x: The x-coordinate of the point.
        :param y: The y-coordinate of the point."""
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
        """Calculate the distance to a point or sprite.
        :param x: The x-coordinate of the point.
        :param y: The y-coordinate of the point.
        :return: The distance to the point or sprite."""
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
        """Remove the sprite from the screen."""
        if self.physics:
            self.physics._remove()
        sprites_group.remove(self)

    @property
    def width(self):
        """Get the width of the sprite.
        :return: The width of the sprite."""
        return self.rect.width

    @property
    def height(self):
        """Get the height of the sprite.
        :return: The height of the sprite."""
        return self.rect.height

    @property
    def right(self):
        """Get the right of the sprite.
        :return: The right of the sprite."""
        return self.x + self.width / 2

    @right.setter
    def right(self, x):
        """Set the right of the sprite to a x-coordinate.
        :param x: The x-coordinate to set the right of the sprite to."""
        self.x = x - self.width / 2

    @property
    def left(self):
        """Get the left of the sprite.
        :return: The left of the sprite."""
        return self.x - self.width / 2

    @left.setter
    def left(self, x):
        """Set the left of the sprite to a x-coordinate.
        :param x: The x-coordinate to set the left of the sprite to."""
        self.x = x + self.width / 2

    @property
    def top(self):
        """Get the top of the sprite.
        :return: The top of the sprite."""
        return self.y + self.height / 2

    @top.setter
    def top(self, y):
        """Set the top of the sprite to a y-coordinate.
        :param y: The y-coordinate to set the top of the sprite to."""
        self.y = y - self.height / 2

    @property
    def bottom(self):
        """Get the bottom of the sprite.
        :return: The bottom of the sprite."""
        return self.y - self.height / 2

    @bottom.setter
    def bottom(self, y):
        """Set the bottom of the sprite to a y-coordinate.
        :param y: The y-coordinate to set the bottom of the sprite to."""
        self.y = y + self.height / 2

    def _pygame_x(self):
        return self.x + (screen.width / 2.0) - (self.rect.width / 2.0)

    def _pygame_y(self):
        return (screen.height / 2.0) - self.y - (self.rect.height / 2.0)

    # @decorator
    def when_clicked(self, callback, call_with_sprite=False):
        """Run a function when the sprite is clicked.
        :param callback: The function to run.
        :param call_with_sprite: Whether to call the function with the sprite as an argument.
        """
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

    def when_touching(self, *sprites):
        """Run a function when the sprite is touching another sprite.
        :param sprites: The sprites to check if they're touching.
        """

        def decorator(func):
            async_callback = _make_async(func)

            async def wrapper(*args, **kwargs):
                wrapper.is_running = True
                await async_callback(*args, **kwargs)
                wrapper.is_running = False

            wrapper.is_running = False

            for sprite in sprites:
                print(sprite)
                sprite._dependent_sprites.append(self)
                self._when_touching_callbacks.append((wrapper, sprite))
            self._when_touching_callbacks = frozenset(self._when_touching_callbacks)
            print(self._when_touching_callbacks)
            return wrapper

        return decorator

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
        """Clone the sprite.
        :return: The cloned sprite."""
        # TODO: make work with physics
        return self.__class__(image=self.image)

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
        """Start the physics simulation for this sprite.
        :param can_move: Whether the object can move.
        :param stable: Whether the object is stable.
        :param x_speed: The x-speed of the object.
        :param y_speed: The y-speed of the object.
        :param obeys_gravity: Whether the object obeys gravity.
        :param bounciness: The bounciness of the object.
        :param mass: The mass of the object.
        :param friction: The friction of the object.
        """
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
        """Stop the physics simulation for this sprite."""
        self.physics._remove()
        self.physics = None
