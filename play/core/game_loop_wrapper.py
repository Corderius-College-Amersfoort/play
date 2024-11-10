"""
This module contains a decorator that listens to exceptions in the game loop.
"""

from ..io.logging import play_logger
from ..loop import loop as _loop


# @decorator
def listen_to_failure():
    """
    A decorator that listens to exceptions in the game loop.
    """

    def decorate(f):
        def applicator(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                _loop.stop()
                play_logger.critical(
                    f"Error in {f.__name__}: {e}"
                )  # pylint: disable=logging-fstring-interpolation
                raise e

        return applicator

    return decorate
