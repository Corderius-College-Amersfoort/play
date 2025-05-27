"""This module contains the mouse loop."""

from ..callback import callback_manager, CallbackType
from ..callback.callback_helpers import run_callback


class MouseState:  # pylint: disable=too-few-public-methods
    click_happened_this_frame = False  # pylint: disable=invalid-name
    click_release_happened_this_frame = False  # pylint: disable=invalid-name


mouse_state = MouseState()


async def _handle_mouse_loop():
    """Handle mouse events in the game loop."""
    ####################################
    # @mouse.when_clicked callbacks
    ####################################
    if (
        mouse_state.click_happened_this_frame
        and callback_manager.get_callbacks(CallbackType.WHEN_CLICKED) is not None
    ):
        for callback in callback_manager.get_callbacks(CallbackType.WHEN_CLICKED):
            run_callback(
                callback,
                [],
                [],
            )

    ########################################
    # @mouse.when_click_released callbacks
    ########################################
    if (
        mouse_state.click_release_happened_this_frame
        and callback_manager.get_callbacks(CallbackType.WHEN_CLICK_RELEASED) is not None
    ):
        for callback in callback_manager.get_callbacks(
            CallbackType.WHEN_CLICK_RELEASED
        ):
            run_callback(
                callback,
                [],
                [],
            )
