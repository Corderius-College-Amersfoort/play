"""This module contains all the objects that can be used in the game window.
Each object is a subclass of Sprite, which is a subclass of pygame.sprite.Sprite.
The objects are: Box, Circle, Line, Text, and Group.
Each object has a corresponding new_* function that can be used to create the object.
For example, play.new_box() creates a new Box object.
"""


from statistics import mean as _mean
from .box import Box, new_box
from .circle import Circle, new_circle
from .line import Line, new_line
from .sprite import Sprite
from .text import Text, new_text


class _MetaGroup(type):
    def __iter__(cls):
        # items added via class variables, e.g.
        #   class Button(play.Group):
        #      text = play.new_text('click me')
        for item in cls.__dict__.values():
            if isinstance(item, Sprite):
                yield item

    def __getattr__(cls, attr):
        """
        E.g.
            class group(play.Group):
                t = play.new_text()
            group.move(10) # calls move(10) on all the group's sprites
        """

        def get_attr(*args, **kwargs): # pylint: disable=inconsistent-return-statements
            results = []
            for sprite in cls: # pylint: disable=not-an-iterable
                result = getattr(sprite, attr)
                if callable(result):
                    result(*args, **kwargs)
                else:
                    results.append(attr)
            if results:
                return results

        return get_attr

    @property
    def x(cls):
        return _mean(sprite.x for sprite in cls) # pylint: disable=not-an-iterable

    @x.setter
    def x(cls, new_x):
        x_offset = new_x - cls.x
        for sprite in cls: # pylint: disable=not-an-iterable
            sprite.x += x_offset

    @property
    def y(cls):
        return _mean(sprite.y for sprite in cls) # pylint: disable=not-an-iterable

    @y.setter
    def y(cls, new_y):
        y_offset = new_y - cls.y
        for sprite in cls: # pylint: disable=not-an-iterable
            sprite.y += y_offset


class Group(metaclass=_MetaGroup):
    """
    A way to group sprites together. A group can either be made like this:

        class button(play.Group):
            bg = play.new_box(width=60, height=30)
            text = play.new_text('hi')

    or like this:

        bg = play.new_box(width=60, height=30)
        text = play.new_text('hi')
        button = play.new_group(bg, text)

    TODO:
        - Button.move() (make work with instance or class)
        - Button.angle = 10 (sets all sprite's angles to 10 in group)
        - for sprite in Button: (make iteration work)
        - play.new_group(bg=bg, text=text) (add keyword args)
        - group.append(), group.remove()?
    """

    def __init__(self, *sprites):
        self.sprites_ = sprites

    @classmethod
    def sprites(cls):
        for item in cls.__dict__.values():
            # items added via class variables, e.g.
            # class Button(play.Group):
            #     text = play.new_text('click me')
            if isinstance(item, Sprite):
                yield item

    def sprites(self): # pylint: disable=function-redefined
        for sprite in self.sprites_:
            yield sprite
        print(self.__class__.sprites)
        for sprite in type(self).sprites():
            yield sprite

    def __iter__(self):
        for sprite in self.sprites: # pylint: disable=not-an-iterable
            yield sprite

    def go_to(self, x_or_sprite, y):
        try:
            x = x_or_sprite.x
            y = x_or_sprite.y
        except AttributeError:
            x = x_or_sprite

        max_x = max(sprite.x for sprite in self)
        min_x = min(sprite.x for sprite in self)
        max_y = max(sprite.y for sprite in self)
        min_y = min(sprite.y for sprite in self)

        center_x = (max_x - min_x) / 2
        center_y = (min_y - max_y) / 2
        offset_x = x - center_x
        offset_y = y - center_y

        for sprite in self:
            sprite.x += offset_x
            sprite.y += offset_y

    @property
    def right(self):
        return max(sprite.right for sprite in self)

    @property
    def left(self):
        return min(sprite.left for sprite in self)

    @property
    def width(self):
        return self.right - self.left


def new_group(*sprites):
    return Group(*sprites)


def new_image(image=None, x=0, y=0, size=100, angle=0, transparency=100): # pylint: disable=too-many-arguments
    return Sprite(
        image=image, x=x, y=y, size=size, angle=angle, transparency=transparency
    )
