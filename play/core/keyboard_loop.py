import pygame

from ..callback import callback_manager, CallbackType
from ..io.keypress import (
    key_num_to_name as _pygame_key_to_name,
    _keys_released_this_frame,
    _keys_to_skip,
    _pressed_keys,
)  # don't pollute user-facing namespace with library internals

def handle_keyboard_events(event):
    if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
        if event.key not in _keys_to_skip:
            name = _pygame_key_to_name(event)
            if name not in _pressed_keys:
                _pressed_keys.append(name)
    if event.type == pygame.KEYUP:  # pylint: disable=no-member
        name = _pygame_key_to_name(event)
        if not (event.key in _keys_to_skip) and name in _pressed_keys:
            _keys_released_this_frame.append(name)
            _pressed_keys.remove(name)

async def handle_keyboard():
    """Handle keyboard events in the game loop."""
    ############################################################
    # @when_any_key_pressed and @when_key_pressed callbacks
    ############################################################
    await callback_manager.run_callbacks_with_filter(
        CallbackType.PRESSED_KEYS, _pressed_keys, ["key"]
    )

    ############################################################
    # @when_any_key_released and @when_key_released callbacks
    ############################################################
    await callback_manager.run_callbacks_with_filter(
        CallbackType.RELEASED_KEYS, _keys_released_this_frame, ["key"]
    )