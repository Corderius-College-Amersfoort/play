import pygame
from .sprite import Sprite
from ..all_sprites import all_sprites
from ..exceptions import Hmm
import warnings as _warnings
from ..color import color_name_to_rgb as _color_name_to_rgb


class Text(Sprite):
    def __init__(self, words='hi :)', x=0, y=0, font=None, font_size=50, color='black', angle=0, transparency=100,
                 size=100):
        super().__init__(x, y, size, angle, transparency)
        self._words = words
        self._x = x
        self._y = y
        self._font = font
        self._font_size = font_size
        self._color = color
        self._size = size
        self._angle = angle
        self.transparency = transparency

        self._is_clicked = False
        self._is_hidden = False
        self.physics = None

        self._compute_primary_surface()

        self._when_clicked_callbacks = []

        all_sprites.append(self)

    def clone(self):
        return self.__class__(words=self.words, font=self.font, font_size=self.font_size, color=self.color,
                              **self._common_properties())

    def _compute_primary_surface(self):
        try:
            self._pygame_font = pygame.font.Font(self._font, self._font_size)
        except:
            _warnings.warn(f"""We couldn't find the font file '{self._font}'. We'll use the default font instead for now.
To fix this, either set the font to None, or make sure you have a font file (usually called something like Arial.ttf) in your project folder.\n""",
                           Hmm)
            self._pygame_font = pygame.font.Font(None, self._font_size)

        self._primary_pygame_surface = self._pygame_font.render(self._words, True, _color_name_to_rgb(self._color))
        self._should_recompute_primary_surface = False

        self._compute_secondary_surface(force=True)

    @property
    def words(self):
        return self._words

    @words.setter
    def words(self, string):
        self._words = str(string)
        self._should_recompute_primary_surface = True

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font_name):
        self._font = str(font_name)
        self._should_recompute_primary_surface = True

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        self._font_size = size
        self._should_recompute_primary_surface = True

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color_):
        self._color = color_
        self._should_recompute_primary_surface = True


def new_text(words='hi :)', x=0, y=0, font=None, font_size=50, color='black', angle=0, transparency=100, size=100):
    return Text(words=words, x=x, y=y, font=font, font_size=font_size, color=color, angle=angle,
                transparency=transparency, size=size)