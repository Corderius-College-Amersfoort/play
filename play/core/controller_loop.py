"""This module contains the controller loop, which handles controller events in the game loop."""

import pygame  # pylint: disable=import-error

from ..callback import callback_manager, CallbackType
from ..io.controllers import (
    controllers,
)
from ..callback.callback_helpers import run_callback

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


def _handle_controller():  # pylint: disable=too-many-branches
    """Handle controller events in the game loop."""
    ############################################################
    # @controller.when_button_pressed and @controller.when_any_button_pressed
    ############################################################
    global controller_button_pressed, controller_button_released, controller_axis_moved
    if controller_button_pressed and callback_manager.get_callbacks(
        CallbackType.WHEN_CONTROLLER_BUTTON_PRESSED
    ):
        controller_button_callbacks = callback_manager.get_callbacks(
            CallbackType.WHEN_CONTROLLER_BUTTON_PRESSED
        )
        if "any" in controller_button_callbacks:
            for callback in controller_button_callbacks["any"]:
                for button in range(controllers.get_numbuttons(callback.controller)):
                    if (
                        controllers.get_controller(callback.controller).get_button(
                            button
                        )
                        == 1
                    ):
                        run_callback(callback, ["button_number"], [], button)
        for button, callbacks in controller_button_callbacks.items():
            if button != "any":
                for callback in callbacks:
                    if controllers.get_button(callback.controller, button) == 1:
                        run_callback(callback, ["button_number"], [], [], button)
        controller_button_pressed = False
    ############################################################
    # @controller.when_button_released
    ############################################################
    if controller_button_released and callback_manager.get_callbacks(
        CallbackType.WHEN_CONTROLLER_BUTTON_RELEASED
    ):
        released_callbacks = callback_manager.get_callbacks(
            CallbackType.WHEN_CONTROLLER_BUTTON_RELEASED
        )
        if "any" in released_callbacks:
            for callback in released_callbacks["any"]:
                for button in range(controllers.get_numbuttons(callback.controller)):
                    if (
                        controllers.get_controller(callback.controller).get_button(
                            button
                        )
                        == 0
                    ):
                        run_callback(callback, ["button_number"], [], button)
        for button, callbacks in released_callbacks.items():
            for callback in callbacks:
                if controllers.get_button(callback.controller, button) == 0:
                    run_callback(callback, ["button_number"], [], button)
        controller_button_released = False
    ############################################################
    # @controller.when_axis_moved
    ############################################################
    if controller_axis_moved and callback_manager.get_callbacks(
        CallbackType.WHEN_CONTROLLER_AXIS_MOVED
    ):
        axis_moved_callbacks = callback_manager.get_callbacks(
            CallbackType.WHEN_CONTROLLER_AXIS_MOVED
        )
        if "any" in axis_moved_callbacks:
            for callback in axis_moved_callbacks["any"]:
                for axis in range(controllers.get_numaxes(callback.controller)):
                    run_callback(
                        callback,
                        ["axis_number", "axis_value"],
                        [],
                        axis,
                        controllers.get_axis(callback.controller, axis),
                    )
        for axis, callbacks in axis_moved_callbacks.items():
            if axis != "any":
                for callback in callbacks:
                    run_callback(
                        callback,
                        ["axis_number", "axis_value"],
                        [],
                        axis,
                        controllers.get_axis(callback.controller, axis),
                    )
        controller_axis_moved = False
