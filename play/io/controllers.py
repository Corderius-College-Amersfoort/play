"""This module contains the controllers class and the controllers object."""

import pygame.joystick
from pygame.joystick import (
    Joystick as _Controller,
    JoystickType as _ControllerType,
    get_count as _get_controller_count,
)

from ..callback import callback_manager, CallbackType
from ..utils.async_helpers import make_async
from ..callback.callback_helpers import run_async_callback

pygame.joystick.init()


def _when_button(index: int, released: bool, *buttons: list[int | list[int]] | None):
    """A decorator that runs a function when a button on a controller is pressed.
    :param index: The index of the controller.
    :param button: The index of the button.
    :return: The function to run."""
    if isinstance(buttons, list):
        for button in buttons:
            if not isinstance(button, int) and not (
                isinstance(button, list) and (not released)
            ):
                raise ValueError("Key must be an integer or a list of integers.")
            if isinstance(button, list):
                for sub_key in button:
                    if not isinstance(sub_key, int):
                        raise ValueError(
                            "Key must be an integer or a list of integers."
                        )

    def decorator(func):
        async_callback = make_async(func)

        async def any_wrapper(button_cb):
            any_wrapper.is_running = True
            await run_async_callback(async_callback, ["button"], [], button_cb)
            any_wrapper.is_running = False

        any_wrapper.is_running = False
        any_wrapper.controller = index

        async def wrapper(button_cb):
            wrapper.is_running = True
            await run_async_callback(async_callback, [], [], ["button"], button_cb)
            wrapper.is_running = False

        wrapper.is_running = False
        wrapper.controller = index

        for button in buttons:
            if button == "any":
                if released:
                    callback_manager.add_callback(
                        CallbackType.WHEN_CONTROLLER_BUTTON_RELEASED, any_wrapper, "any"
                    )
                else:
                    callback_manager.add_callback(
                        CallbackType.WHEN_CONTROLLER_BUTTON_PRESSED, any_wrapper, "any"
                    )
                continue
            if isinstance(button, list):
                button = hash(frozenset(button))
            if released:
                callback_manager.add_callback(
                    CallbackType.WHEN_CONTROLLER_BUTTON_RELEASED, wrapper, button
                )
            else:
                callback_manager.add_callback(
                    CallbackType.WHEN_CONTROLLER_BUTTON_PRESSED, wrapper, button
                )
        return wrapper

    return decorator


class _Controllers:
    def __init__(self):
        self._controllers = [_Controller(x) for x in range(_get_controller_count())]
        for controller in self._controllers:
            controller.init()

    def get_count(self) -> int:
        """Get the number of controllers.
        :return: The number of controllers."""
        return len(self._controllers)

    def get_controller(self, index) -> _ControllerType:
        """Get the controller at the specified index.
        :param index: The index of the controller.
        :return: The controller at the specified index."""
        return self._controllers[index]

    def get_all_controllers(self) -> list[_ControllerType]:
        """Get all controllers.
        :return: A list of all controllers."""
        return self._controllers

    def get_num_axes(self, index) -> int:
        """Get the number of axes on the controller at the specified index.
        :param index: The index of the controller.
        :return: The number of axes on the controller at the specified index."""
        return self._controllers[index].get_numaxes()

    def get_axis(self, index, axis) -> float:
        """Get the value of the specified axis on the controller at the specified index.
        :param index: The index of the controller.
        :param axis: The index of the axis.
        :return: The value of the specified axis on the controller at the specified index.
        """
        return self._controllers[index].get_axis(axis)

    def get_num_buttons(self, index) -> int:
        """Get the number of buttons on the controller at the specified index.
        :param index: The index of the controller.
        :return: The number of buttons on the controller at the specified index."""
        return self._controllers[index].get_numbuttons()

    def get_button(self, index, button) -> int:
        """Get the value of the specified button on the controller at the specified index.
        :param index: The index of the controller.
        :param button: The index of the button.
        :return: The value of the specified button on the controller at the specified index.
        """
        return self._controllers[index].get_button(button)

    def get_num_hats(self, index) -> int:
        """Get the number of hats on the controller at the specified index.
        :param index: The index of the controller.
        :return: The number of hats on the controller at the specified index."""
        return self._controllers[index].get_numhats()

    def get_hat(self, index, hat) -> tuple[int, int]:
        """Get the value of the specified hat on the controller at the specified index.
        :param index: The index of the controller.
        :param hat: The index of the hat.
        :return: The value of the specified hat on the controller at the specified index.
        """
        return self._controllers[index].get_hat(hat)

    def get_num_balls(self, index) -> int:
        """Get the number of balls on the controller at the specified index.
        :param index: The index of the controller.
        :return: The number of balls on the controller at the specified index."""
        return self._controllers[index].get_numballs()

    def get_ball(self, index, ball) -> tuple[float, float]:
        """Get the value of the specified ball on the controller at the specified index.
        :param index: The index of the controller.
        :param ball: The index of the ball.
        :return: The value of the specified ball on the controller at the specified index.
        """
        return self._controllers[index].get_ball(ball)

    # @decorator
    def when_button_pressed(self, index, *buttons):
        """A decorator that runs a function when a button on a controller is pressed.
        :param index: The index of the controller.
        :param button: The index of the button.
        :return: The function to run."""
        return _when_button(index, False, *buttons)

    # @decorator
    def when_any_button_pressed(self, index):
        """A decorator that runs a function when any button on a controller is pressed.
        :param index: The index of the controller.
        :return: The function to run."""
        buttons = {"any": None}
        return _when_button(index, False, *buttons)

    # @decorator
    def when_button_released(self, index, *buttons):
        """A decorator that runs a function when a button on a controller is released.
        :param index: The index of the controller.
        :param button: The index of the button.
        :return: The function to run."""
        return _when_button(index, True, *buttons)

    # @decorator
    def when_any_button_released(self, index):
        """A decorator that runs a function when any button on a controller is released.
        :param index: The index of the controller.
        :return: The function to run."""
        buttons = {"any": None}
        return _when_button(index, True, *buttons)

    # @decorator
    def when_axis_moved(self, index, axis):
        """A decorator that runs a function when an axis on a controller is moved.
        :param index: The index of the controller.
        :param axis: The index of the axis.
        :return: The function to run."""

        def decorator(func):
            async_callback = make_async(func)

            async def wrapper(axis, value):
                wrapper.is_running = True
                await run_async_callback(
                    async_callback, ["axis", "value"], [], axis, value
                )
                wrapper.is_running = False

            wrapper.is_running = False
            wrapper.axis = axis
            wrapper.controller = index

            callback_manager.add_callback(
                CallbackType.WHEN_CONTROLLER_AXIS_MOVED, wrapper, axis
            )
            return wrapper

        return decorator

    # @decorator
    def when_any_axis_moved(self, index):
        """A decorator that runs a function when any axis on a controller is moved.
        :param index: The index of the controller.
        :return: The function to run."""

        def decorator(func):
            async_callback = make_async(func)

            async def wrapper(axis, value):
                wrapper.is_running = True
                await run_async_callback(
                    async_callback, ["axis", "value"], [], axis, value
                )
                wrapper.is_running = False

            wrapper.is_running = False
            wrapper.axis = None
            wrapper.controller = index

            callback_manager.add_callback(
                CallbackType.WHEN_CONTROLLER_AXIS_MOVED, wrapper
            )
            return wrapper

        return decorator


controllers = _Controllers()
