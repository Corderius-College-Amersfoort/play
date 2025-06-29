"""
This module contains the CallbackManager class and CallbackType enum.
"""

from enum import Enum

from play.callback.callback_helpers import run_callback, run_async_callback


class CallbackType(Enum):
    REPEAT_FOREVER = 0
    WHEN_PROGRAM_START = 1
    PRESSED_KEYS = 2
    RELEASED_KEYS = 3
    WHEN_CLICKED = 4
    WHEN_CLICK_RELEASED = 5
    WHEN_CLICKED_SPRITE = 6
    WHEN_TOUCHING = 7
    WHEN_STOPPED_TOUCHING = 8
    WHEN_TOUCHING_WALL = 9
    WHEN_STOPPED_TOUCHING_WALL = 10
    WHEN_CONTROLLER_BUTTON_PRESSED = 11
    WHEN_CONTROLLER_BUTTON_RELEASED = 12
    WHEN_CONTROLLER_AXIS_MOVED = 13
    WHEN_RESIZED = 14


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

    def run_callbacks(
        self,
        callback_type,
        *args,
        callback_discriminator=None,
        **kwargs,
    ):
        """
        Run all callbacks of a certain type with the given arguments.
        :param callback_type: The type of callback.
        :param callback_discriminator: The discriminator for the callback.
        :param args: Positional arguments to pass to the callbacks.
        :param kwargs: Keyword arguments to pass to the callbacks.
        :return: None
        """
        if callback_type not in self.callbacks:
            return

        if callback_discriminator is not None:
            if callback_discriminator not in self.callbacks[callback_type]:
                return

            for callback in self.callbacks[callback_type][callback_discriminator]:
                if callable(callback) and (hasattr(callback, "is_running") is False):
                    run_callback(callback, args, kwargs)
        else:
            for callback in self.callbacks[callback_type]:
                if callable(callback) and (hasattr(callback, "is_running") is False):
                    run_callback(callback, args, kwargs)

    async def run_callbacks_with_filter(  # pylint: disable=keyword-arg-before-vararg,dangerous-default-value,too-many-branches
        self,
        callback_type,
        activated_states,
        required_args=None,
        optional_args=None,
        property_filter={},
        *args,
    ):
        """
        Run callbacks of a certain type with a specific discriminator.
        :param callback_type: The type of callback.
        :param activated_states: The states to filter by.
        :param required_args: The required arguments for the callback.
        :param optional_args: The optional arguments for the callback.
        :param property_filter: A dictionary of properties to filter the callbacks. For example, {'controller': 0}.
        :return: None
        """
        if required_args is None:
            required_args = []
        if optional_args is None:
            optional_args = []

        def is_valid_callback(cb):
            if not callable(cb):
                return False
            if hasattr(cb, "is_running") and cb.is_running:
                return False

            if property_filter:
                for key, value in property_filter.items():
                    if (
                        getattr(cb, key, None) != value
                        and getattr(cb, key, None) != "any"
                    ):
                        return False
            return True

        if not activated_states or not self.get_callbacks(callback_type):
            return

        subscriptions = self.get_callbacks(callback_type)
        for state in activated_states:
            if state in subscriptions:
                for callback in subscriptions[state]:
                    if not is_valid_callback(callback):
                        continue

                    await run_async_callback(
                        callback, required_args, optional_args, state, *args
                    )
            if "any" in subscriptions:
                for callback in subscriptions["any"]:
                    if not is_valid_callback(callback):
                        continue

                    await run_async_callback(
                        callback, required_args, optional_args, state, *args
                    )
        all_hash = hash(frozenset(activated_states))
        if all_hash in subscriptions:
            for callback in subscriptions[all_hash]:
                if not is_valid_callback(callback):
                    continue

                await run_async_callback(
                    callback,
                    required_args,
                    optional_args,
                    activated_states,
                    *args,
                )


callback_manager = CallbackManager()
