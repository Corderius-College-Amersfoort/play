"""Generators for creating new objects."""

from ..objects import Box, Circle, Line, Text, Sprite


def new_text(  # pylint: disable=too-many-arguments
    words="hi :)",
    x=0,
    y=0,
    font=None,
    font_size=50,
    color="black",
    angle=0,
    transparency=100,
    size=100,
):
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
    return Text(
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
    color="black",
    x=0,
    y=0,
    width=100,
    height=200,
    border_color="light blue",
    border_width=0,
    angle=0,
    transparency=100,
    size=100,
):
    """Make a new box object.
    :param color: The color of the box.
    :param x: The x-coordinate of the box.
    :param y: The y-coordinate of the box.
    :param width: The width of the box.
    :param height: The height of the box.
    :param border_color: The color of the border of the box.
    :param border_width: The width of the border of the box.
    :param angle: The angle of the box.
    :param transparency: The transparency of the box.
    :param size: The size of the box.
    :return: A new box object.
    """
    return Box(
        color=color,
        x=x,
        y=y,
        width=width,
        height=height,
        border_color=border_color,
        border_width=border_width,
        angle=angle,
        transparency=transparency,
        size=size,
    )


def new_circle(  # pylint: disable=too-many-arguments
    color="black",
    x=0,
    y=0,
    radius=100,
    border_color="light blue",
    border_width=0,
    transparency=100,
    size=100,
    angle=0,
):
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
    return Circle(
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
    color="black",
    x=0,
    y=0,
    length=None,
    angle=None,
    thickness=1,
    x1=None,
    y1=None,
    transparency=100,
    size=100,
):
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
    return Line(
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


def new_image(
    image=None, x=0, y=0, size=100, angle=0, transparency=100
):  # pylint: disable=too-many-arguments
    """Make a new image object.
    :param image: The image to display.
    :param x: The x-coordinate of the image.
    :param y: The y-coordinate of the image.
    :param size: The size of the image.
    :param angle: The angle of the image.
    :param transparency: The transparency of the image.
    :return: A new image object.
    """
    return Sprite(
        image=image, x=x, y=y, size=size, angle=angle, transparency=transparency
    )
