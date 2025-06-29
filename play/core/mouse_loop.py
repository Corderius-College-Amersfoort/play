"""This module contains the mouse loop."""

import pygame

from ..callback import callback_manager, CallbackType
from ..io.mouse import mouse
from ..io.screen import screen


class MouseState:  # pylint: disable=too-few-public-methods
    click_happened_this_frame = False  # pylint: disable=invalid-name
    click_release_happened_this_frame = False  # pylint: disable=invalid-name


mouse_state = MouseState()


def handle_mouse_events(event):
    """Handle mouse events and update the mouse state."""
    if event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
        mouse_state.click_happened_this_frame = True
        mouse._is_clicked = True
    if event.type == pygame.MOUSEBUTTONUP:  # pylint: disable=no-member
        mouse_state.click_release_happened_this_frame = True
        mouse._is_clicked = False
    if event.type == pygame.MOUSEMOTION:  # pylint: disable=no-member
        mouse.x, mouse.y = (event.pos[0] - screen.width / 2.0), (
            screen.height / 2.0 - event.pos[1]
        )


async def handle_mouse_loop():
    """Handle mouse events in the game loop."""
    ####################################
    # @mouse.when_clicked callbacks
    ####################################
    if mouse_state.click_happened_this_frame:
        callback_manager.run_callbacks(
            CallbackType.WHEN_CLICKED,
            [],
            [],
        )

    ########################################
    # @mouse.when_click_released callbacks
    ########################################
    if mouse_state.click_release_happened_this_frame:
        callback_manager.run_callbacks(
            CallbackType.WHEN_CLICK_RELEASED,
            [],
            [],
        )
