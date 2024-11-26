"""
This module contains helper functions for running callback functions.
"""

import asyncio as _asyncio
import inspect

from ..loop import loop as _loop


def run_callback(callback, required_args, optional_args, *args, **kwargs):
    """
    Run a callback function with the given arguments.
    :param callback: The callback function to run.
    :param required_args: The required arguments for the callback function.
    :param optional_args: The optional arguments for the callback function.
    :param args: The arguments to pass to the callback function.
    :param kwargs: The keyword arguments to pass to the callback
    :return: The result of the callback function.
    """
    # check if callback takes in the required number of arguments
    if not _asyncio.iscoroutinefunction(callback):
        raise ValueError("The callback function must be an async function.")
    actual_args = inspect.getfullargspec(callback).args
    if (
        len(required_args)
        <= len(actual_args)
        <= len(required_args) + len(optional_args)
    ):
        callback_args = args[: len(actual_args)]
        _loop.create_task(callback(*callback_args, **kwargs))
    else:
        if len(required_args) == 0:
            raise ValueError(
                f"The callback function must not take in any arguments.\n"
                f"On line {callback.__code__.co_firstlineno} in {callback.__code__.co_filename}"
            )
        raise ValueError(
            f"The callback function must take in {len(required_args)} argument(s):\n"
            f"Required: {required_args}\n"
            f"{len(optional_args)} optional argument(s): {optional_args}\n"
            f"On line {callback.__code__.co_firstlineno} in {callback.__code__.co_filename}"
        )


async def run_async_callback(callback, required_args, optional_args, *args, **kwargs):
    """
    Run a callback function with the given arguments.
    :param callback: The callback function to run.
    :param required_args: The required arguments for the callback function.
    :param optional_args: The optional arguments for the callback function.
    :param args: The arguments to pass to the callback function.
    :param kwargs: The keyword arguments to pass to the callback
    :return: The result of the callback function.
    """
    # check if callback takes in the required number of arguments
    if not _asyncio.iscoroutinefunction(callback):
        raise ValueError("The callback function must be an async function.")
    actual_cb = callback
    if hasattr(callback, "original_function"):
        actual_cb = callback.original_function
    actual_args = inspect.getfullargspec(actual_cb).args
    if (
        len(required_args)
        <= len(actual_args)
        <= len(required_args) + len(optional_args)
    ):
        callback_args = args[: len(actual_args)]
        await callback(*callback_args, **kwargs)
    else:
        if len(required_args) == 0:
            raise ValueError(
                f"The callback function must not take in any arguments.\n"
                f"On line {actual_cb.__code__.co_firstlineno} in {actual_cb.__code__.co_filename}"
            )
        raise ValueError(
            f"The callback function must take in {len(required_args)} argument(s):\n"
            f"Required: {required_args}\n"
            f"{len(optional_args)} optional argument(s): {optional_args}\n"
            f"On line {actual_cb.__code__.co_firstlineno} in {actual_cb.__code__.co_filename}"
        )
