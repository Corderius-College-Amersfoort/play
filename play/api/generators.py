"""Generators for creating new objects."""

from ..objects import (
    Box as _Box,
    Circle as _Circle,
    Line as _Line,
    Text as _Text,
    Image as _Image,
)


def new_text(  # pylint: disable=too-many-arguments
    words: str = "",
    x: int = 0,
    y: int = 0,
    font: str = "/path/to/font",
    font_size: int = 50,
    color: str = "black",
    angle: int = 0,
    transparency: int = 100,
    size: int = 100,
) -> _Text:
    """Make a new text object.
    :param words: The text to display.
    :param x: The x-coordinate of the text.
    :param y: The y-coordinate of the text.
    :param font: The font to use.
    :param font_size: The size of the font.
    :param color: The color of the text.
    :param angle: The angle of the text.
    :param transparency: The transparency of the text.
    :param size: The size of the text.
    :return: A new text object.
    """
    if not isinstance(words, str):
        raise TypeError("words for a text object must be a string")

    return _Text(
        words=words,
        x=x,
        y=y,
        font=font,
        font_size=font_size,
        color=color,
        angle=angle,
        transparency=transparency,
        size=size,
    )


def new_box(  # pylint: disable=too-many-arguments
    color: str = "black",
    x: int = 0,
    y: int = 0,
    width: int = 100,
    height: int = 200,
    border_color: str = "light blue",
    border_width: int = 0,
    border_radius: int = 0,
    angle: int = 0,
    transparency: int = 100,
    size: int = 100,
) -> _Box:
    """Make a new box object.
    :param color: The color of the box.
    :param x: The x-coordinate of the box.
    :param y: The y-coordinate of the box.
    :param width: The width of the box.
    :param height: The height of the box.
    :param border_color: The color of the border of the box.
    :param border_width: The width of the border of the box.
    :param border_radius: The radius of the border (rounding).
    :param angle: The angle of the box.
    :param transparency: The transparency of the box.
    :param size: The size of the box.
    :return: A new box object.
    """
    return _Box(
        color=color,
        x=x,
        y=y,
        width=width,
        height=height,
        border_color=border_color,
        border_width=border_width,
        border_radius=border_radius,
        angle=angle,
        transparency=transparency,
        size=size,
    )


def new_circle(  # pylint: disable=too-many-arguments
    color: str = "black",
    x: int = 0,
    y: int = 0,
    radius: int = 100,
    border_color: str = "light blue",
    border_width: int = 0,
    transparency: int = 100,
    size: int = 100,
    angle: int = 0,
) -> _Circle:
    """Make a new circle object.
    :param color: The color of the circle.
    :param x: The x-coordinate of the circle.
    :param y: The y-coordinate of the circle.
    :param radius: The radius of the circle.
    :param border_color: The color of the border of the circle.
    :param border_width: The width of the border of the circle.
    :param transparency: The transparency of the circle.
    :param size: The size of the circle.
    :param angle: The angle of the circle.
    :return: A new circle object.
    """
    return _Circle(
        color=color,
        x=x,
        y=y,
        radius=radius,
        border_color=border_color,
        border_width=border_width,
        transparency=transparency,
        size=size,
        angle=angle,
    )


def new_line(  # pylint: disable=too-many-arguments
    color: str = "black",
    x: int = 0,
    y: int = 0,
    length=None,
    angle=None,
    thickness: int = 1,
    x1=None,
    y1=None,
    transparency: int = 100,
    size: int = 100,
) -> _Line:
    """Make a new line object.
    :param color: The color of the line.
    :param x: The x-coordinate of the line.
    :param y: The y-coordinate of the line.
    :param length: The length of the line.
    :param angle: The angle of the line.
    :param thickness: The thickness of the line.
    :param x1: The x-coordinate of the second point of the line.
    :param y1: The y-coordinate of the second point of the line.
    :param transparency: The transparency of the line.
    :param size: The size of the line.
    :return: A new line object.
    """
    return _Line(
        color=color,
        x=x,
        y=y,
        length=length,
        angle=angle,
        thickness=thickness,
        x1=x1,
        y1=y1,
        transparency=transparency,
        size=size,
    )


def new_image(  # pylint: disable=too-many-arguments
    image: str = "/path/to/image",
    x: int = 0,
    y: int = 0,
    size: int = 100,
    angle: int = 0,
    transparency: int = 100,
) -> _Image:
    """Make a new image object.
    :param image: The image to display.
    :param x: The x-coordinate of the image.
    :param y: The y-coordinate of the image.
    :param size: The size of the image.
    :param angle: The angle of the image.
    :param transparency: The transparency of the image.
    :return: A new image object.
    """
    return _Image(
        image=image, x=x, y=y, size=size, angle=angle, transparency=transparency
    )
