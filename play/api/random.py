"""Generate random numbers, colors, and positions."""

import random as _random

from ..io import screen
from ..utils import _Position


def random_number(lowest=0, highest=100):
    """Return a random number between `lowest` and `highest`.
    :param lowest: The lowest number that can be returned.
    :param highest: The highest number that can be returned.
    :return: A random number between `lowest` and `highest`.
    """
    # if user supplies whole numbers, return whole numbers
    if isinstance(lowest, int) and isinstance(highest, int):
        return _random.randint(lowest, highest)
    # if user supplied any floats, return decimals
    return round(_random.uniform(lowest, highest), 2)


def random_color():
    """Return a random color.
    :return: A random color.
    """
    return random_number(0, 255), random_number(0, 255), random_number(0, 255)


def random_position(
    x_min=screen.left, x_max=screen.right, y_min=screen.bottom, y_max=screen.top
):
    """
    Returns a random position on the screen. A position has an `x` and `y` e.g.:
        position = play.random_position()
        sprite.x = position.x
        sprite.y = position.y

    or equivalently:
        sprite.go_to(play.random_position())
    """
    return _Position(
        random_number(x_min, x_max),
        random_number(y_min, y_max),
    )
