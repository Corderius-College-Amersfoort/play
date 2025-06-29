"""Keyboard event handling for the game loop."""
import pygame

from ..callback import callback_manager, CallbackType
from ..io.keypress import (
    key_num_to_name as _pygame_key_to_name,
    keyboard_state,
    KEYS_TO_SKIP,
)


def handle_keyboard_events(event):
    """Handle keyboard events and update the keyboard state."""
    if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
        if event.key not in KEYS_TO_SKIP:
            name = _pygame_key_to_name(event)
            if name not in keyboard_state.pressed_keys:
                keyboard_state.pressed_keys.append(name)
    if event.type == pygame.KEYUP:  # pylint: disable=no-member
        name = _pygame_key_to_name(event)
        if not (event.key in KEYS_TO_SKIP) and name in keyboard_state.pressed_keys:
            keyboard_state.keys_released.append(name)
            keyboard_state.pressed_keys.remove(name)


async def handle_keyboard():
    """Handle keyboard events in the game loop."""
    ############################################################
    # @when_any_key_pressed and @when_key_pressed callbacks
    ############################################################
    await callback_manager.run_callbacks_with_filter(
        CallbackType.PRESSED_KEYS, keyboard_state.pressed_keys, ["key"]
    )

    ############################################################
    # @when_any_key_released and @when_key_released callbacks
    ############################################################
    await callback_manager.run_callbacks_with_filter(
        CallbackType.RELEASED_KEYS, keyboard_state.keys_released, ["key"]
    )
