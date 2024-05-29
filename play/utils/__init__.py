"""A bunch of random math functions."""

from ..globals import COLOR_NAMES
from ..io.exceptions import Oops


def _clamp(num, min_, max_):
    if num < min_:
        return min_
    if num > max_:
        return max_
    return num


class _Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, indices):
        if indices == 0:
            return self.x
        if indices == 1:
            return self.y
        raise IndexError()

    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self):
        return 2

    def __setitem__(self, i, value):
        if i == 0:
            self.x = value
        elif i == 1:
            self.y = value
        else:
            raise IndexError()


def color_name_to_rgb(name):
    """
    Turn an English color name into an RGB value.

    lightBlue
    light-blue
    light blue

    are all valid and will produce the rgb value for lightblue.
    """
    if isinstance(name, tuple):
        return name

    try:
        return COLOR_NAMES[name.lower().strip().replace("-", "").replace(" ", "")]
    except KeyError as exception:
        raise Oops(
            f"""You gave a color name we didn't understand: '{name}'
If this our mistake, please let us know. Otherwise, try using the RGB number form of the color e.g. '(0, 255, 255)'.
You can find the RGB form of a color on websites like this: https://www.rapidtables.com/web/color/RGB_Color.html\n"""
        ) from exception
