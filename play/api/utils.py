"""Game functions and utilities."""

import asyncio as _asyncio
import logging as _logging

import pygame  # pylint: disable=import-error

from .events import _when_program_starts_callbacks, _game_loop, _loop
from ..utils import color_name_to_rgb as _color_name_to_rgb
from ..globals import backdrop as _backdrop
from ..io.keypress import _pressed_keys

BACKDROP = _backdrop


def start_program():
    """
    Calling this function starts your program running.

    play.start_program() should almost certainly go at the very end of your program.
    """
    for func in _when_program_starts_callbacks:
        _loop.create_task(func())

    _loop.call_soon(_game_loop)
    try:
        _loop.run_forever()
    finally:
        _logging.getLogger("asyncio").setLevel(_logging.CRITICAL)
        pygame.quit()  # pylint: disable=no-member


async def animate():
    await _asyncio.sleep(0)


def set_backdrop(color_or_image_name):
    """Set the backdrop color or image for the game.
    :param color_or_image_name: The color or image to set as the backdrop.
    """
    global BACKDROP
    _color_name_to_rgb(color_or_image_name)

    BACKDROP = color_or_image_name


async def timer(seconds=1.0):
    """Wait a number of seconds. Used with the await keyword like this:

    @play.repeat_forever
    async def do():
        await play.timer(seconds=2)
        print('hi')
    :param seconds: The number of seconds to wait.
    :return: True after the number of seconds has passed.
    """
    await _asyncio.sleep(seconds)
    return True


def key_is_pressed(*keys):
    """
    Returns True if any of the given keys are pressed.

    Example:

        @play.repeat_forever
        async def do():
            if play.key_is_pressed('up', 'w'):
                print('up or w pressed')
    """
    # Called this function key_is_pressed instead of is_key_pressed so it will
    # sound more english-like with if-statements:
    #
    #   if play.key_is_pressed('w', 'up'): ...

    for key in keys:
        if key in _pressed_keys.values():
            return True
    return False