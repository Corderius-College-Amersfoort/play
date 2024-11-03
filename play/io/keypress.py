"""This module contains functions and decorators for handling key presses."""

import pygame

from ..utils.async_helpers import _make_async

pygame.key.set_repeat(200, 16)

_pressed_keys_subscriptions = {}
_release_keys_subscriptions = {}

_pressed_keys = []

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
        if "any" not in _release_keys_subscriptions:
            _release_keys_subscriptions["any"] = []
        _release_keys_subscriptions["any"].append(wrapper)
    else:
        if "any" not in _pressed_keys_subscriptions:
            _pressed_keys_subscriptions["any"] = []
        _pressed_keys_subscriptions["any"].append(wrapper)
    return wrapper


def when_key(*keys, released=False):
    """Run a function when a key is pressed or released."""
    for key in keys:
        if not isinstance(key, str) and not (isinstance(key, list) and (not released)):
            print(key)
            raise ValueError("Key must be a string or a list of strings.")
        if isinstance(key, list):
            for sub_key in key:
                if not isinstance(sub_key, str):
                    raise ValueError("Key must be a string or a list of strings.")

    def decorator(func):
        async_callback = _make_async(func)

        async def wrapper(*args, **kwargs):
            wrapper.is_running = True
            await async_callback(*args, **kwargs)
            wrapper.is_running = False

        wrapper.is_running = False

        for key in keys:
            if isinstance(key, list):
                key = hash(frozenset(key))
            if released:
                if key not in _release_keys_subscriptions:
                    _release_keys_subscriptions[key] = []
                _release_keys_subscriptions[key].append(wrapper)
            else:
                if key not in _pressed_keys_subscriptions:
                    _pressed_keys_subscriptions[key] = []
                _pressed_keys_subscriptions[key].append(wrapper)
        return wrapper

    return decorator


def key_num_to_name(pygame_key_event):
    """Convert a pygame key event to a human-readable string."""
    return pygame.key.name(pygame_key_event.key)
