"""This module contains functions and decorators for handling key presses."""

import pygame

from ..callback import callback_manager, CallbackType
from ..utils.async_helpers import make_async
from ..callback.callback_helpers import run_async_callback

pygame.key.set_repeat(200, 16)

_pressed_keys = []

_keys_released_this_frame = []
_keys_to_skip = (pygame.K_MODE,)


def when_any_key(func, released=False):
    """Run a function when any key is pressed or released."""
    async_callback = make_async(func)

    async def wrapper(key):
        wrapper.is_running = True
        await run_async_callback(async_callback, ["key"], [], key)
        wrapper.is_running = False

    wrapper.keys = None
    wrapper.is_running = False
    if released:
        callback_manager.add_callback(CallbackType.RELEASED_KEYS, wrapper, "any")
    else:
        callback_manager.add_callback(CallbackType.PRESSED_KEYS, wrapper, "any")
    return wrapper


def when_key(*keys, released=False):
    """Run a function when a key is pressed or released."""
    for control_key in keys:
        if not isinstance(control_key, str) and not (isinstance(control_key, list)):
            raise ValueError("Key must be a string or a list of strings.")
        if isinstance(control_key, list):
            for sub_key in control_key:
                if not isinstance(sub_key, str):
                    raise ValueError("Key must be a string or a list of strings.")

    def decorator(func):
        async_callback = make_async(func)

        async def wrapper(active_key):
            wrapper.is_running = True
            await run_async_callback(async_callback, [], ["key"], active_key)
            wrapper.is_running = False

        wrapper.is_running = False

        for key in keys:
            if isinstance(key, list):
                key = hash(frozenset(key))
            if released:
                callback_manager.add_callback(CallbackType.RELEASED_KEYS, wrapper, key)
            else:
                callback_manager.add_callback(CallbackType.PRESSED_KEYS, wrapper, key)
        return wrapper

    return decorator


def key_num_to_name(pygame_key_event):
    """Convert a pygame key event to a human-readable string."""
    return pygame.key.name(pygame_key_event.key)
