"""Game functions and utilities."""

import asyncio as _asyncio
import logging as _logging

import pygame  # pylint: disable=import-error

from .events import _when_program_starts_callbacks, _game_loop
from ..loop import loop as _loop
from ..utils import color_name_to_rgb as _color_name_to_rgb
from ..io.keypress import _pressed_keys
from ..globals import backdrop as __backdrop

_backdrop = __backdrop  # Work around for the global variable not being imported


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


def stop_program():
    """
    Calling this function stops your program running.

    play.stop_program() should almost certainly go at the very end of your program.
    """
    _loop.stop()
    pygame.quit()  # pylint: disable=no-member


async def animate():
    """
    Wait for the next frame to be drawn.
    """
    await _asyncio.sleep(0)


def set_backdrop(color_or_image_name):
    """Set the backdrop color or image for the game.
    :param color_or_image_name: The color or image to set as the backdrop.
    """
    global _backdrop
    _color_name_to_rgb(color_or_image_name)

    _backdrop = color_or_image_name


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

    for key in keys:
        if key in _pressed_keys.values():
            return True
    return False
