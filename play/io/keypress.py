"""This module contains functions and decorators for handling key presses."""

import asyncio as _asyncio

import pygame

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


# pylint: enable=no-member

def key_num_to_name(pygame_key_event):
    """Convert a pygame key event to a human-readable string."""
    return pygame.key.name(pygame_key_event.key)
