"""This module contains functions and decorators for handling key presses."""

import asyncio as _asyncio

import pygame

from ..utils.async_helpers import _make_async

pygame.key.set_repeat(200, 16)
_pressed_keys = {}
_keypress_callbacks = []
_keyrelease_callbacks = []

_loop = _asyncio.get_event_loop()
_loop.set_debug(False)

_keys_pressed_this_frame = []
_keys_released_this_frame = []
_keys_to_skip = (pygame.K_MODE,)
pygame.event.set_allowed(
    [
        pygame.QUIT,
        pygame.KEYDOWN,
        pygame.KEYUP,
        pygame.MOUSEBUTTONDOWN,
        pygame.MOUSEBUTTONUP,
        pygame.MOUSEMOTION,
    ]
)


def when_any_key(func, released=False):
    """Run a function when any key is pressed or released."""
    async_callback = _make_async(func)

    async def wrapper(*args, **kwargs):
        wrapper.is_running = True
        await async_callback(*args, **kwargs)
        wrapper.is_running = False

    wrapper.keys = None
    wrapper.is_running = False
    if released:
        _keyrelease_callbacks.append(wrapper)
    else:
        _keypress_callbacks.append(wrapper)
    return wrapper


def when_key(*keys, released=False):
    """Run a function when a key is pressed or released."""
    def decorator(func):
        async_callback = _make_async(func)

        async def wrapper(*args, **kwargs):
            wrapper.is_running = True
            await async_callback(*args, **kwargs)
            wrapper.is_running = False

        wrapper.keys = keys
        wrapper.is_running = False
        if released:
            _keyrelease_callbacks.append(wrapper)
        else:
            _keypress_callbacks.append(wrapper)
        return wrapper

    return decorator


def key_num_to_name(pygame_key_event):
    """Convert a pygame key event to a human-readable string."""
    return pygame.key.name(pygame_key_event.key)
