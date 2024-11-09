import pygame  # pylint: disable=import-error
from ..loop import loop as _loop
from ..io.controllers import (
    controllers,
    _when_button_pressed_subscriptions,
    _when_button_released_subscriptions,
    _when_axis_moved_subscriptions
)
from ..utils.callback_helpers import run_callback

controller_axis_moved = False  # pylint: disable=invalid-name
controller_button_pressed = False  # pylint: disable=invalid-name
controller_button_released = False  # pylint: disable=invalid-name

def _handle_controller_events(event):
    """Handle controller events in the game loop.
    :param event: The event to handle."""
    if event.type == pygame.JOYAXISMOTION:  # pylint: disable=no-member
        global controller_axis_moved
        controller_axis_moved = True
    if event.type == pygame.JOYBUTTONDOWN:  # pylint: disable=no-member
        global controller_button_pressed
        controller_button_pressed = True
    if event.type == pygame.JOYBUTTONUP:
        global controller_button_released
        controller_button_released = True

def _handle_controller():
    """Handle controller events in the game loop."""
    ############################################################
    # @controller.when_button_pressed and @controller.when_any_button_pressed
    ############################################################
    global controller_button_pressed, controller_button_released, controller_axis_moved
    if controller_button_pressed and _when_button_pressed_subscriptions:
        if "any" in _when_button_pressed_subscriptions:
            for callback in _when_button_pressed_subscriptions["any"]:
                for button in range(controllers.get_numbuttons(callback.controller)):
                    if controllers.get_controller(callback.controller).get_button(button) == 1:
                        run_callback(
                            callback,
                            "The callback function must take in 1 argument: button_number",
                            button
                        )
        for button,callbacks in _when_button_pressed_subscriptions.items():
            if button != "any":
                for callback in callbacks:
                    if controllers.get_button(callback.controller, button) == 1:
                        run_callback(
                            callback,
                            "The callback function must take in 1 argument: button_number",
                            button
                        )
        controller_button_pressed = False
    ############################################################
    # @controller.when_button_released
    ############################################################
    if controller_button_released and _when_button_released_subscriptions:
        if "any" in _when_button_released_subscriptions:
            for callback in _when_button_released_subscriptions["any"]:
                for button in range(controllers.get_numbuttons(callback.controller)):
                    if controllers.get_controller(callback.controller).get_button(button) == 0:
                        run_callback(
                            callback,
                            "The callback function must take in 1 argument: button_number",
                            button
                        )
        for button,callbacks in _when_button_released_subscriptions.items():
            for callback in callbacks:
                if controllers.get_button(callback.controller, button) == 0:
                    run_callback(
                        callback,
                        "The callback function must take in 1 argument: button_number",
                        button
                    )
        controller_button_released = False
    ############################################################
    # @controller.when_axis_moved
    ############################################################
    if controller_axis_moved and _when_axis_moved_subscriptions:
        if "any" in _when_axis_moved_subscriptions:
            for callback in _when_axis_moved_subscriptions["any"]:
                for axis in range(controllers.get_numaxes(callback.controller)):
                    run_callback(
                        callback,
                        "The callback function must take in 2 arguments: axis_number, axis_value",
                        axis, controllers.get_axis(callback.controller, axis)
                    )
        for axis,callbacks in _when_axis_moved_subscriptions.items():
            if axis != "any":
                for callback in callbacks:
                    run_callback(
                        callback,
                        "The callback function must take in 2 arguments: axis_number, axis_value",
                        axis, controllers.get_axis(callback.controller, axis)
                    )
        controller_axis_moved = False

