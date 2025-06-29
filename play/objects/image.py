"""This module contains the Image class, which is a subclass of the Sprite class."""

import os
import pygame

from .sprite import Sprite
from ..io.screen import convert_pos


class Image(Sprite):
    def __init__(self, image, x=0, y=0, angle=0, size=100, transparency=100):
        super().__init__()
        if isinstance(image, str):
            if not os.path.isfile(image):
                raise FileNotFoundError(f"Image file '{image}' not found.")
            image = pygame.image.load(image)
        self._image = image
        self._original_width = self._image.get_width()
        self._original_height = self._image.get_height()
        self._x = x
        self._y = y
        self._angle = angle
        self._size = size
        self._transparency = transparency
        self.rect = self._image.get_rect()
        self.update()

    def update(self):
        """Update the image's position, size, angle, and transparency."""
        if self._should_recompute:
            draw_image = pygame.transform.scale(
                self._image,
                (
                    self._original_width * self._size // 100,
                    self._original_height * self._size // 100,
                ),
            )
            draw_image = pygame.transform.rotate(draw_image, self.angle)
            draw_image.set_alpha(self.transparency * 2.55)
            self.rect = draw_image.get_rect()
            pos = convert_pos(self.x, self.y)
            self.rect.center = pos
            super().update()

    @property
    def image(self):
        """Return the image."""
        return self._image

    @image.setter
    def image(self, image: str):
        """Set the image."""
        if not os.path.isfile(image):
            raise FileNotFoundError(f"Image file '{image}' not found.")
        self._image = pygame.image.load(image)
        self.update()
