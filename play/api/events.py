"""All the events that can be triggered in the game."""

import logging as _logging

import pygame  # pylint: disable=import-error
from play.core import (
    game_loop as _game_loop,
    _repeat_forever_callbacks,
    _when_program_starts_callbacks,
)
from ..io.keypress import (
    when_key as _when_key,
    when_any_key as _when_any_key,
)
from ..io.mouse import mouse
from ..utils.async_helpers import _make_async
from ..loop import loop as _loop


# @decorator
def when_program_starts(func):
    """
    Call code right when the program starts.

    Used like this:

    @play.when_program_starts
    def do():
        print('the program just started!')
    :param func: The function to call when the program starts.
    :return: The decorator function.
    """
    async_callback = _make_async(func)

    async def wrapper(*args, **kwargs):
        return await async_callback(*args, **kwargs)

    _when_program_starts_callbacks.append(wrapper)
    return func


def repeat(number_of_times):
    """
    Repeat a set of commands a certain number of times.

    Equivalent to `range(1, number_of_times+1)`.

    Used like this:

    @play.repeat_forever
    async def do():
        for count in play.repeat(10):
            print(count)
    :param number_of_times: The number of times to repeat the commands.
    :return: A range object that can be iterated over.
    """
    return range(1, number_of_times + 1)


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


# @decorator
def repeat_forever(func):
    """
    Calls the given function repeatedly in the game loop.

    Example:

        text = play.new_text(words='hi there!', x=0, y=0, font='Arial.ttf', font_size=20, color='black')

        @play.repeat_forever
        async def do():
            text.turn(degrees=15)
    :param func: The function to call repeatedly.
    :return: The decorator function.
    """
    async_callback = _make_async(func)

    async def repeat_wrapper():
        repeat_wrapper.is_running = True
        await async_callback()
        repeat_wrapper.is_running = False

    repeat_wrapper.is_running = False
    _repeat_forever_callbacks.append(repeat_wrapper)
    return func


# @decorator
def when_sprite_clicked(*sprites):
    """A decorator that runs a function when a sprite is clicked.
    :param sprites: The sprites to run the function on.
    :return: The function to run.
    """

    def wrapper(func):
        for sprite in sprites:
            sprite.when_clicked(func, call_with_sprite=True)
        return func

    return wrapper


# @decorator
def when_any_key_pressed(func):
    """
    Calls the given function when any key is pressed.
    """
    if not callable(func):
        raise ValueError(
            """@play.when_any_key_pressed doesn't use a list of keys. Try just this instead:

@play.when_any_key_pressed
async def do(key):
    print("This key was pressed!", key)
"""
        )
    return _when_any_key(func, released=False)


# @decorator
def when_key_pressed(*keys):
    """
    Calls the given function when any of the specified keys are pressed.
    """
    return _when_key(*keys, released=False)


# @decorator
def when_any_key_released(func):
    """
    Calls the given function when any key is released.
    """
    if not callable(func):
        raise ValueError(
            """@play.when_any_key_released doesn't use a list of keys. Try just this instead:

@play.when_any_key_released
async def do(key):
    print("This key was released!", key)
"""
        )
    return _when_any_key(func, released=True)


# @decorator
def when_key_released(*keys):
    """
    Calls the given function when any of the specified keys are released.
    """
    return _when_key(*keys, released=True)


# @decorator
def when_mouse_clicked(func):
    """
    Calls the given function when the mouse is clicked.
    """
    return mouse.when_clicked(func)


# @decorator
def when_click_released(func):
    """
    Calls the given function when the mouse click is released.
    """
    return mouse.when_click_released(func)
