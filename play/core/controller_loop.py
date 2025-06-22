"""This module contains the controller loop, which handles controller events in the game loop."""

import pygame  # pylint: disable=import-error

from ..callback import callback_manager, CallbackType
from ..io.controllers import (
    controllers,
)
from ..callback.callback_helpers import run_async_callback

controller_axis_moved = False  # pylint: disable=invalid-name
controller_button_pressed = False  # pylint: disable=invalid-name
controller_button_released = False  # pylint: disable=invalid-name


def handle_controller_events(event):
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


async def handle_controller():  # pylint: disable=too-many-branches
    """Handle controller events in the game loop."""
    ############################################################
    # @controller.when_button_pressed and @controller.when_any_button_pressed
    ############################################################
    global controller_button_pressed, controller_button_released, controller_axis_moved
    if controller_button_pressed:
        for controller in controllers.get_controllers():
            controller_buttons_pressed = controllers.get_controller(
                controller
            ).get_buttons_pressed()
            callback_manager.run_callbacks_with_filter(
                CallbackType.WHEN_CONTROLLER_BUTTON_PRESSED,
                controller_buttons_pressed,
                ["button_number"],
                [],
                {"controller": controller},
            )
        controller_button_pressed = False

    ############################################################
    # @controller.when_button_released
    ############################################################
    if controller_button_released:
        for controller in controllers.get_controllers():
            controller_buttons_released = controllers.get_controller(
                controller
            ).get_buttons_released()
            callback_manager.run_callbacks_with_filter(
                CallbackType.WHEN_CONTROLLER_BUTTON_RELEASED,
                controller_buttons_released,
                ["button_number"],
                [],
                {"controller": controller},
            )
        controller_button_released = False
    ############################################################
    # @controller.when_axis_moved
    ############################################################
    if controller_axis_moved:
        for controller in controllers.get_controllers():
            controller_axis_moved = controllers.get_controller(
                controller
            ).get_axis_moved()
            callback_manager.run_callbacks_with_filter(
                CallbackType.WHEN_CONTROLLER_AXIS_MOVED,
                controller_axis_moved,
                ["axis_number", "value"],
                [],
                {"controller": controller},
            )
        controller_axis_moved = False
