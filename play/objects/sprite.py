from ..all_sprites import all_sprites
import pygame
from ..exceptions import Oops, Hmm
import os as _os
import math as _math
import pymunk as _pymunk
from ..physics import physics_space, _Physics
import warnings as _warnings
from ..clamp import _clamp
from ..io import screen
from ..async_helpers import _make_async


def _sprite_touching_sprite(a, b):
    # todo: custom code for circle, line, rotated rectangley sprites
    # use physics engine if both sprites have physics on
    # if a.physics and b.physics:
    if a.left >= b.right or a.right <= b.left or a.top <= b.bottom or a.bottom >= b.top: return False
    return True


def _point_touching_sprite(point, sprite):
    # todo: custom code for circle, line, rotated rectangley sprites
    return sprite.left <= point.x <= sprite.right and sprite.bottom <= point.y <= sprite.top


class Sprite(object):
    def __init__(self, image=None, x=0, y=0, size=100, angle=0, transparency=100):
        self._image = image or _os.path.join(_os.path.split(__file__)[0], 'blank_image.png')
        self._x = x
        self._y = y
        self._angle = angle
        self._size = size
        self._transparency = transparency

        self.physics = None
        self._is_clicked = False
        self._is_hidden = False

        self._compute_primary_surface()

        self._when_clicked_callbacks = []

        all_sprites.append(self)

    def _compute_primary_surface(self):
        try:
            self._primary_pygame_surface = pygame.image.load(_os.path.join(self._image))
        except pygame.error as exc:
            raise Oops(f"""We couldn't find the image file you provided named "{self._image}".
If the file is in a folder, make sure you add the folder name, too.""") from exc
        self._primary_pygame_surface.set_colorkey((255, 255, 255, 255))  # set background to transparent

        self._should_recompute_primary_surface = False

        # always recompute secondary surface if the primary surface changes
        self._compute_secondary_surface(force=True)

    def _compute_secondary_surface(self, force=False):

        self._secondary_pygame_surface = self._primary_pygame_surface.copy()

        # transparency
        if self._transparency != 100 or force:
            try:
                # for text and images with transparent pixels
                array = pygame.surfarray.pixels_alpha(self._secondary_pygame_surface)
                array[:, :] = (array[:, :] * (self._transparency / 100.)).astype(
                    array.dtype)  # modify surface pixels in-place
                del array  # I think pixels are written when array leaves memory, so delete it explicitly here
            except Exception as e:
                # this works for images without alpha pixels in them
                self._secondary_pygame_surface.set_alpha(round((self._transparency / 100.) * 255))

        # scale
        if (self.size != 100) or force:
            ratio = self.size / 100.
            self._secondary_pygame_surface = pygame.transform.scale(
                self._secondary_pygame_surface,
                (round(self._secondary_pygame_surface.get_width() * ratio),  # width
                 round(self._secondary_pygame_surface.get_height() * ratio)))  # height

        # rotate
        if (self.angle != 0) or force:
            self._secondary_pygame_surface = pygame.transform.rotate(self._secondary_pygame_surface, self._angle)

        self._should_recompute_secondary_surface = False

    @property
    def is_clicked(self):
        return self._is_clicked

    def move(self, steps=3):
        angle = _math.radians(self.angle)
        self.x += steps * _math.cos(angle)
        self.y += steps * _math.sin(angle)

    def turn(self, degrees=10):
        self.angle += degrees

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, _x):
        prev_x = self._x
        self._x = _x
        if self.physics:
            self.physics._pymunk_body.position = self._x, self._y
            if prev_x != _x:
                # setting velocity makes the simulation more realistic usually
                self.physics._pymunk_body.velocity = _x - prev_x, self.physics._pymunk_body.velocity.y
            if self.physics._pymunk_body.body_type == _pymunk.Body.STATIC:
                physics_space.reindex_static()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, _y):
        prev_y = self._y
        self._y = _y
        if self.physics:
            self.physics._pymunk_body.position = self._x, self._y
            if prev_y != _y:
                # setting velocity makes the simulation more realistic usually
                self.physics._pymunk_body.velocity = self.physics._pymunk_body.velocity.x, _y - prev_y
            if self.physics._pymunk_body.body_type == _pymunk.Body.STATIC:
                physics_space.reindex_static()

    @property
    def transparency(self):
        return self._transparency

    @transparency.setter
    def transparency(self, alpha):
        if not isinstance(alpha, float) and not isinstance(alpha, int):
            raise Oops(f"""Looks like you're trying to set {self}'s transparency to '{alpha}', which isn't a number.
Try looking in your code for where you're setting transparency for {self} and change it a number.
""")
        if alpha > 100 or alpha < 0:
            _warnings.warn(f"""The transparency setting for {self} is being set to {alpha} and it should be between 0 and 100.
You might want to look in your code where you're setting transparency and make sure it's between 0 and 100.  """, Hmm)

        self._transparency = _clamp(alpha, 0, 100)
        self._should_recompute_secondary_surface = True

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image_filename):
        self._image = image_filename
        self._should_recompute_primary_surface = True

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, _angle):
        self._angle = _angle
        self._should_recompute_secondary_surface = True

        if self.physics:
            self.physics._pymunk_body.angle = _math.radians(_angle)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, percent):
        self._size = percent
        self._should_recompute_secondary_surface = True
        if self.physics:
            self.physics._remove()
            self.physics._make_pymunk()

    def hide(self):
        self._is_hidden = True
        if self.physics:
            self.physics.pause()

    def show(self):
        self._is_hidden = False
        if self.physics:
            self.physics.unpause()

    @property
    def is_hidden(self):
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, hide):
        self._is_hidden = hide

    @property
    def is_shown(self):
        return not self._is_hidden

    @is_shown.setter
    def is_shown(self, show):
        self._is_hidden = not show

    def is_touching(self, sprite_or_point):
        rect = self._secondary_pygame_surface.get_rect()
        if isinstance(sprite_or_point, Sprite):
            return _sprite_touching_sprite(sprite_or_point, self)
        else:
            return _point_touching_sprite(sprite_or_point, self)

    def point_towards(self, x, y=None):
        try:
            x, y = x.x, x.y
        except AttributeError:
            x, y = x, y
        self.angle = _math.degrees(_math.atan2(y - self.y, x - self.x))

    def go_to(self, x=None, y=None):
        """
        Example:

            # text will follow around the mouse
            text = play.new_text('yay')

            @play.repeat_forever
            async def do():
                text.go_to(play.mouse)
        """
        assert (not x is None)

        try:
            # users can call e.g. sprite.go_to(play.mouse), so x will be an object with x and y
            self.x = x.x
            self.y = x.y
        except AttributeError:
            self.x = x
            self.y = y

    def distance_to(self, x, y=None):
        assert (not x is None)

        try:
            # x can either be a number or a sprite. If it's a sprite:
            x1 = x.x
            y1 = x.y
        except AttributeError:
            x1 = x
            y1 = y

        dx = self.x - x1
        dy = self.y - y1

        return _math.sqrt(dx ** 2 + dy ** 2)

    def remove(self):
        if self.physics:
            self.physics._remove()
        all_sprites.remove(self)

    @property
    def width(self):
        return self._secondary_pygame_surface.get_width()

    @property
    def height(self):
        return self._secondary_pygame_surface.get_height()

    @property
    def right(self):
        return self.x + self.width / 2

    @right.setter
    def right(self, x):
        self.x = x - self.width / 2

    @property
    def left(self):
        return self.x - self.width / 2

    @left.setter
    def left(self, x):
        self.x = x + self.width / 2

    @property
    def top(self):
        return self.y + self.height / 2

    @top.setter
    def top(self, y):
        self.y = y - self.height / 2

    @property
    def bottom(self):
        return self.y - self.height / 2

    @bottom.setter
    def bottom(self, y):
        self.y = y + self.height / 2

    def _pygame_x(self):
        return self.x + (screen.width / 2.) - (self._secondary_pygame_surface.get_width() / 2.)

    def _pygame_y(self):
        return (screen.height / 2.) - self.y - (self._secondary_pygame_surface.get_height() / 2.)

    # @decorator
    def when_clicked(self, callback, call_with_sprite=False):
        async_callback = _make_async(callback)

        async def wrapper():
            wrapper.is_running = True
            if call_with_sprite:
                await async_callback(self)
            else:
                await async_callback()
            wrapper.is_running = False

        wrapper.is_running = False
        self._when_clicked_callbacks.append(wrapper)
        return wrapper

    def _common_properties(self):
        # used with inheritance to clone
        return {'x': self.x, 'y': self.y, 'size': self.size, 'transparency': self.transparency, 'angle': self.angle}

    def clone(self):
        # TODO: make work with physics
        return self.__class__(image=self.image, **self._common_properties())

    # def __getattr__(self, key):
    #     # TODO: use physics as a proxy object so users can do e.g. sprite.x_speed
    #     if not self.physics:
    #         return getattr(self, key)
    #     else:
    #         return getattr(self.physics, key)

    # def __setattr__(self, name, value):
    #     if not self.physics:
    #         return setattr(self, name, value)
    #     elif self.physics and name in :
    #         return setattr(self.physics, name, value)

    def start_physics(self, can_move=True, stable=False, x_speed=0, y_speed=0, obeys_gravity=True, bounciness=1.0,
                      mass=10, friction=0.1):
        if not self.physics:
            self.physics = _Physics(
                self,
                can_move,
                stable,
                x_speed,
                y_speed,
                obeys_gravity,
                bounciness,
                mass,
                friction,
            )

    def stop_physics(self):
        self.physics._remove()
        self.physics = None
