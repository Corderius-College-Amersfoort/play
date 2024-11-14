"""This module contains code to help with async functions."""

import asyncio as _asyncio
import warnings as _warnings

from play.io.logging import play_logger


def _raise_on_await_warning(func):
    """
    If someone doesn't put 'await' before functions that require 'await'
    like play.timer() or play.animate(), raise an exception.
    :param func: A function that may or may not be async
    """

    async def raise_on_warning(*args, **kwargs):
        with _warnings.catch_warnings(record=True) as warnings:
            await func(*args, **kwargs)
            for warning in warnings:
                str_message = warning.message.args[
                    0
                ]  # e.g. "coroutine 'timer' was never awaited"
                if "was never awaited" in str_message:
                    unawaited_function_name = str_message.split("'")[1]

                    play_logger.warning(
                        f"""Looks like you forgot to put "await" before play.{unawaited_function_name}"""
                        + f"""on line {warning.lineno} of file {warning.filename}.
To fix this, just add the word 'await' before play.{unawaited_function_name}"""
                        + f"""on line {warning.lineno} of file {warning.filename} in the function {func.__name__}."""
                    )  # pylint: disable=logging-not-lazy
                play_logger.warning(warning.message)

    raise_on_warning.original_function = func
    return raise_on_warning


def _make_async(func):
    """
    Turn a non-async function into an async function.
    Used mainly in decorators like @repeat_forever.
    :param func: A function that may or may not be async.
    """
    if _asyncio.iscoroutinefunction(func):
        # if it's already async just return it
        return _raise_on_await_warning(func)

    @_raise_on_await_warning
    async def async_func(*args, **kwargs):
        return func(*args, **kwargs)

    async_func.original_function = func
    return async_func
