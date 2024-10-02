"""This module contains all the objects that can be used in the game window.
Each object is a subclass of Sprite, which is a subclass of pygame.sprite.Sprite.
The objects are: Box, Circle, Line, Text, and Group.
Each object has a corresponding new_* function that can be used to create the object.
For example, play.new_box() creates a new Box object.
"""

from .box import Box
from .circle import Circle
from .line import Line
from .sprite import Sprite
from .text import Text
from .image import Image
