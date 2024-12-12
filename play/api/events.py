"""All the events that can be triggered in the game."""

from ..callback import callback_manager, CallbackType
from ..io.keypress import (
    when_key as _when_key,
    when_any_key as _when_any_key,
)
from ..io.controllers import controllers
from ..io.mouse import mouse
from ..utils.async_helpers import _make_async
from ..callback.callback_helpers import run_async_callback

_ = controllers  # Work around for the global variable not being imported


# @decorator
def when_program_starts(func):
    """
    Call code right when the program starts.

    Example:

        text = play.new_text(words='hi there!')

        @play.when_program_starts
        def show():
            text.words = 'started'

    :param func: The function to call when the program starts.
    :return: The decorator function.
    """
    async_callback = _make_async(func)

    async def wrapper():
        return await run_async_callback(
            async_callback,
            [],
            [],
        )

    callback_manager.add_callback(CallbackType.WHEN_PROGRAM_START, wrapper)
    return func


# @decorator
def repeat_forever(func):
    """
    Calls the given function repeatedly in the game loop.

    Example:

        text = play.new_text(words='hi there!')

        @play.repeat_forever
        def turn():
            print("this is printing every single frame")


    :param func: The function to call repeatedly.
    :return: The decorator function.
    """
    async_callback = _make_async(func)

    async def repeat_wrapper():
        repeat_wrapper.is_running = True
        await run_async_callback(
            async_callback,
            [],
            [],
        )
        repeat_wrapper.is_running = False

    repeat_wrapper.is_running = False
    callback_manager.add_callback(CallbackType.REPEAT_FOREVER, repeat_wrapper)
    return func


# @decorator
def when_sprite_clicked(*sprites):
    """A decorator that runs a function when a sprite is clicked.

    Example:

        text = play.new_text(words='hi there!')

        @play.when_sprite_clicked(text)
        def show(sprite):
            text.words = 'clicked!'

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

    Example:

        text = play.new_text(words='hi there!')

        @play.when_any_key_pressed
        def show(key):
            text.words = key
    """
    if not callable(func):
        raise ValueError("""@play.when_any_key_pressed doesn't use a list of keys.""")
    return _when_any_key(func, released=False)


# @decorator
def when_key_pressed(*keys):
    """
    Calls the given function when any of the specified keys are pressed.

    Example:

        text = play.new_text(words='hi there!')

        @play.when_key_pressed('a')
        def show(key):
            text.words = key
    """
    return _when_key(*keys, released=False)


# @decorator
def when_any_key_released(func):
    """
    Calls the given function when any key is released.

    Example:

        text = play.new_text(words='hi there!')

        @play.when_any_key_released
        def show(key):
            text.words = key
    """
    if not callable(func):
        raise ValueError("""@play.when_any_key_released doesn't use a list of keys.""")
    return _when_any_key(func, released=True)


# @decorator
def when_key_released(*keys):
    """
    Calls the given function when any of the specified keys are released.

    Example:

        text = play.new_text(words='hi there!')

        @play.when_key_released('a')
        def show(key):
            text.words = key
    """
    return _when_key(*keys, released=True)


# @decorator
def when_mouse_clicked(func):
    """
    Calls the given function when the mouse is clicked.

    Example:
        text = play.new_text(words='hi there!')

        @play.when_mouse_clicked
        def show():
            text.words = 'mouse click'
    """
    return mouse.when_clicked(func)


# @decorator
def when_click_released(func):
    """
    Calls the given function when the mouse click is released.

    Example:
        text = play.new_text(words='hi there!')

        @play.when_click_released
        def show():
            text.words = 'mouse click released'
    """
    return mouse.when_click_released(func)
