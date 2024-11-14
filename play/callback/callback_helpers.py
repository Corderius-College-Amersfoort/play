"""
This module contains helper functions for running callback functions.
"""

import asyncio as _asyncio

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
    if (
        len(required_args)
        <= len(callback.__code__.co_varnames)
        <= len(required_args) + len(optional_args)
    ):
        callback_args = args[: len(callback.__code__.co_varnames)]
        _loop.create_task(callback(*callback_args, **kwargs))
    else:
        if len(required_args) == 0:
            raise ValueError("The callback function must not take in any arguments.")
        raise ValueError(
            f"The callback function must take in {len(required_args)} argument(s):\n"
            f"Required: {required_args}\n"
            f"{len(optional_args)} optional argument(s): {optional_args}"
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
    if (
        len(required_args)
        <= len(actual_cb.__code__.co_varnames)
        <= len(required_args) + len(optional_args)
    ):
        callback_args = args[: len(actual_cb.__code__.co_varnames)]
        await callback(*callback_args, **kwargs)
    else:
        if len(required_args) == 0:
            raise ValueError("The callback function must not take in any arguments.")
        raise ValueError(
            f"The callback function must take in {len(required_args)} argument(s):\n"
            f"Required: {required_args}\n"
            f"{len(optional_args)} optional argument(s): {optional_args}"
        )
