"""This module contains the Mouse class and the mouse object."""

import math as _math

from ..utils.async_helpers import _make_async
from ..objects.sprite import point_touching_sprite


class _Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self._is_clicked = False
        self._when_clicked_callbacks = []
        self._when_click_released_callbacks = []

    @property
    def is_clicked(self):
        """Return whether the mouse is clicked.
        :return: True if the mouse is clicked, False otherwise."""
        return self._is_clicked

    def is_touching(self, other):
        """Check if the mouse is touching a sprite.
        :param other: The sprite to check.
        :return: True if the mouse is touching the sprite, False otherwise."""
        return point_touching_sprite(self, other)

    # @decorator
    def when_clicked(self, func):
        """Run a function when the mouse is clicked.
        :param func: The function to run."""
        async_callback = _make_async(func)

        async def wrapper():
            await async_callback()

        self._when_clicked_callbacks.append(wrapper)
        return wrapper

    # @decorator
    def when_click_released(self, func):
        """Run a function when the mouse click is released.
        :param func: The function to run."""
        async_callback = _make_async(func)

        async def wrapper():
            await async_callback()

        self._when_click_released_callbacks.append(wrapper)
        return wrapper

    def distance_to(self, x=None, y=None):
        """Get the distance from the mouse to a point.
        :param x: The x-coordinate of the point.
        :param y: The y-coordinate of the point.
        :return: The distance from the mouse to the point."""
        assert x is not None

        try:
            # x can either be a number or a sprite. If it's a sprite:
            x = x.x
            y = x.y
        except AttributeError:
            pass

        dx = self.x - x
        dy = self.y - y

        return _math.sqrt(dx**2 + dy**2)


mouse = _Mouse()
