"""This module contains functions and decorators for handling keypresses."""

import asyncio as _asyncio

import pygame

from .exceptions import Oops
from .async_helpers import _make_async

# pylint: disable=no-member
keypress_map = {
    pygame.K_BACKSPACE: "backspace",
    pygame.K_TAB: "tab",
    pygame.K_CLEAR: "clear",
    pygame.K_RETURN: "enter",
    pygame.K_PAUSE: "pause",
    pygame.K_ESCAPE: "escape",
    pygame.K_SPACE: "space",
    pygame.K_EXCLAIM: "!",
    pygame.K_QUOTEDBL: '"',
    pygame.K_HASH: "#",
    pygame.K_DOLLAR: "$",
    pygame.K_AMPERSAND: "&",
    pygame.K_QUOTE: "'",
    pygame.K_LEFTPAREN: "(",
    pygame.K_RIGHTPAREN: ")",
    pygame.K_ASTERISK: "*",
    pygame.K_PLUS: "+",
    pygame.K_COMMA: ",",
    pygame.K_MINUS: "-",
    pygame.K_PERIOD: ".",
    pygame.K_SLASH: "/",
    pygame.K_0: "0",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9",
    pygame.K_COLON: ":",
    pygame.K_SEMICOLON: ";",
    pygame.K_LESS: "<",
    pygame.K_EQUALS: "=",
    pygame.K_GREATER: ">",
    pygame.K_QUESTION: "?",
    pygame.K_AT: "@",
    pygame.K_LEFTBRACKET: "[",
    pygame.K_BACKSLASH: "\\",
    pygame.K_RIGHTBRACKET: "]",
    pygame.K_CARET: "^",
    pygame.K_UNDERSCORE: "_",
    pygame.K_BACKQUOTE: "`",
    pygame.K_a: "a",
    pygame.K_b: "b",
    pygame.K_c: "c",
    pygame.K_d: "d",
    pygame.K_e: "e",
    pygame.K_f: "f",
    pygame.K_g: "g",
    pygame.K_h: "h",
    pygame.K_i: "i",
    pygame.K_j: "j",
    pygame.K_k: "k",
    pygame.K_l: "l",
    pygame.K_m: "m",
    pygame.K_n: "n",
    pygame.K_o: "o",
    pygame.K_p: "p",
    pygame.K_q: "q",
    pygame.K_r: "r",
    pygame.K_s: "s",
    pygame.K_t: "t",
    pygame.K_u: "u",
    pygame.K_v: "v",
    pygame.K_w: "w",
    pygame.K_x: "x",
    pygame.K_y: "y",
    pygame.K_z: "z",
    pygame.K_DELETE: "delete",
    # pygame.K_KP0: '',
    # pygame.K_KP1: '',
    # pygame.K_KP2: '',
    # pygame.K_KP3: '',
    # pygame.K_KP4: '',
    # pygame.K_KP5: '',
    # pygame.K_KP6: '',
    # pygame.K_KP7: '',
    # pygame.K_KP8: '',
    # pygame.K_KP9: '',
    # pygame.K_KP_PERIOD: '',
    # pygame.K_KP_DIVIDE: '',
    # pygame.K_KP_MULTIPLY: '',
    # pygame.K_KP_MINUS: '',
    # pygame.K_KP_PLUS: '',
    # pygame.K_KP_ENTER: '',
    # pygame.K_KP_EQUALS: '',
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_RIGHT: "right",
    pygame.K_LEFT: "left",
    pygame.K_INSERT: "insert",
    pygame.K_HOME: "home",
    pygame.K_END: "end",
    pygame.K_PAGEUP: "pageup",
    pygame.K_PAGEDOWN: "pagedown",
    pygame.K_F1: "F1",
    pygame.K_F2: "F2",
    pygame.K_F3: "F3",
    pygame.K_F4: "F4",
    pygame.K_F5: "F5",
    pygame.K_F6: "F6",
    pygame.K_F7: "F7",
    pygame.K_F8: "F8",
    pygame.K_F9: "F9",
    pygame.K_F10: "F10",
    pygame.K_F11: "F11",
    pygame.K_F12: "F12",
    pygame.K_F13: "F13",
    pygame.K_F14: "F14",
    pygame.K_F15: "F15",
    pygame.K_NUMLOCK: "numlock",
    pygame.K_CAPSLOCK: "capslock",
    pygame.K_SCROLLOCK: "scrollock",
    pygame.K_RSHIFT: "shift",
    pygame.K_LSHIFT: "shift",
    pygame.K_RCTRL: "control",
    pygame.K_LCTRL: "control",
    pygame.K_RALT: "alt",
    pygame.K_LALT: "alt",
    pygame.K_RMETA: "meta",
    pygame.K_LMETA: "meta",
    pygame.K_LSUPER: "super",
    pygame.K_RSUPER: "super",
    # pygame.K_MODE: '',
    # pygame.K_HELP: '',
    # pygame.K_PRINT: '',
    # pygame.K_SYSREQ: '',
    # pygame.K_BREAK: '',
    # pygame.K_MENU: '',
    # pygame.K_POWER: '',
    pygame.K_EURO: "€",
}

pygame.key.set_repeat(200, 16)
_pressed_keys = {}
_keypress_callbacks = []
_keyrelease_callbacks = []


# @decorator
def when_any_key_pressed(func):
    if not callable(func):
        raise Oops(
            """@play.when_any_key_pressed doesn't use a list of keys. Try just this instead:

@play.when_any_key_pressed
async def do(key):
    print("This key was pressed!", key)
"""
        )
    async_callback = _make_async(func)

    async def wrapper(*args, **kwargs):
        wrapper.is_running = True
        await async_callback(*args, **kwargs)
        wrapper.is_running = False

    wrapper.keys = None
    wrapper.is_running = False
    _keypress_callbacks.append(wrapper)
    return wrapper


# @decorator
def when_key_pressed(*keys):
    def decorator(func):
        async_callback = _make_async(func)

        async def wrapper(*args, **kwargs):
            wrapper.is_running = True
            await async_callback(*args, **kwargs)
            wrapper.is_running = False

        wrapper.keys = keys
        wrapper.is_running = False
        _keypress_callbacks.append(wrapper)
        return wrapper

    return decorator


# @decorator
def when_any_key_released(func):
    if not callable(func):
        raise Oops(
            """@play.when_any_key_released doesn't use a list of keys. Try just this instead:

@play.when_any_key_released
async def do(key):
    print("This key was released!", key)
"""
        )
    async_callback = _make_async(func)

    async def wrapper(*args, **kwargs):
        wrapper.is_running = True
        await async_callback(*args, **kwargs)
        wrapper.is_running = False

    wrapper.keys = None
    wrapper.is_running = False
    _keyrelease_callbacks.append(wrapper)
    return wrapper


# @decorator
def when_key_released(*keys):
    def decorator(func):
        async_callback = _make_async(func)

        async def wrapper(*args, **kwargs):
            wrapper.is_running = True
            await async_callback(*args, **kwargs)
            wrapper.is_running = False

        wrapper.keys = keys
        wrapper.is_running = False
        _keyrelease_callbacks.append(wrapper)
        return wrapper

    return decorator


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


def pygame_key_to_name(pygame_key_event):
    english_name = keypress_map[pygame_key_event.key]
    if not pygame_key_event.mod and len(english_name) > 1:
        # use english names like 'space' instead of the space character ' '
        return english_name
    return pygame_key_event.unicode
    # pygame_key_event.unicode is how we get e.g. # instead of 3 on US keyboards when shift+3 is pressed.
    # It also gives us capital letters and things like that.
