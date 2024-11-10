"""
This module contains the CallbackManager class and CallbackType enum.
"""

from enum import Enum


class CallbackType(Enum):
    REPEAT_FOREVER = 0
    WHEN_PROGRAM_START = 1
    PRESSED_KEYS = 2
    RELEASED_KEYS = 3
    WHEN_CLICKED = 4
    WHEN_CLICK_RELEASED = 5
    WHEN_CLICKED_SPRITE = 6
    WHEN_TOUCHING = 7
    WHEN_CONTROLLER_BUTTON_PRESSED = 8
    WHEN_CONTROLLER_BUTTON_RELEASED = 9
    WHEN_CONTROLLER_AXIS_MOVED = 10


class CallbackManager:
    def __init__(self):
        """
        A class to manage callbacks.
        """
        self.callbacks = {}

    def add_callback(
        self, callback_type, callback, callback_discriminator=None
    ) -> None:
        """
        Add a callback to the callback manager.
        :param callback_type: The type of callback.
        :param callback: The callback function.
        :param callback_discriminator: The discriminator for the callback.
        :return: None
        """
        if callback_type not in self.callbacks:
            if callback_discriminator is None:
                self.callbacks[callback_type] = []
            else:
                self.callbacks[callback_type] = {}
        if callback_discriminator is None:
            self.callbacks[callback_type].append(callback)
        else:
            if callback_discriminator not in self.callbacks[callback_type]:
                self.callbacks[callback_type][callback_discriminator] = []
            self.callbacks[callback_type][callback_discriminator].append(callback)

    def get_callbacks(self, callback_type) -> dict:
        """
        Get the callbacks of a certain type.
        :param callback_type: The type of callback.
        :return: The callbacks of the specified type.
        """
        return self.callbacks.get(callback_type, None)

    def get_callback(self, callback_type, callback_discriminator=None) -> callable:
        """
        Get a callback of a certain type.
        :param callback_type: The type of callback.
        :param callback_discriminator: The discriminator for the callback.
        :return: The callback(s) of the specified type.
        """
        if callback_discriminator is None:
            return self.callbacks.get(callback_type, None)
        return self.callbacks.get(callback_type, {}).get(callback_discriminator, None)


callback_manager = CallbackManager()
