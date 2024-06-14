"""All the events that can be triggered in the game."""

import logging as _logging
import math as _math

import pygame  # pylint: disable=import-error

from ..globals import all_sprites, backdrop
from ..io import screen, PYGAME_DISPLAY
from ..io.exceptions import Oops
from ..io.keypress import (
    pygame_key_to_name as _pygame_key_to_name,
    _loop,
    _keys_pressed_this_frame,
    _keys_released_this_frame,
    _keys_to_skip,
    _pressed_keys,
    _keypress_callbacks,
    _keyrelease_callbacks,
)  # don't pollute user-facing namespace with library internals
from ..io.mouse import mouse
from ..objects.line import Line
from ..objects.sprite import point_touching_sprite
from ..physics import simulate_physics
from ..utils import color_name_to_rgb as _color_name_to_rgb
from ..utils.async_helpers import _make_async

_when_program_starts_callbacks = []
_clock = pygame.time.Clock()


# pylint: disable=too-many-branches, too-many-statements
def _game_loop():
    _keys_pressed_this_frame.clear()  # do this instead of `_keys_pressed_this_frame = []` to save a tiny bit of memory
    _keys_released_this_frame.clear()
    click_happened_this_frame = False
    click_release_happened_this_frame = False

    _clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (  # pylint: disable=no-member
                event.type == pygame.KEYDOWN  # pylint: disable=no-member
                and event.key == pygame.K_q  # pylint: disable=no-member
                and (
                        pygame.key.get_mods() & pygame.KMOD_META  # pylint: disable=no-member
                        or pygame.key.get_mods() & pygame.KMOD_CTRL  # pylint: disable=no-member
                )
        ):
            # quitting by clicking window's close button or pressing ctrl+q / command+q
            _loop.stop()
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
            click_happened_this_frame = True
            mouse._is_clicked = True
        if event.type == pygame.MOUSEBUTTONUP:  # pylint: disable=no-member
            click_release_happened_this_frame = True
            mouse._is_clicked = False
        if event.type == pygame.MOUSEMOTION:  # pylint: disable=no-member
            mouse.x, mouse.y = (event.pos[0] - screen.width / 2.0), (
                    screen.height / 2.0 - event.pos[1]
            )
        if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            if event.key not in _keys_to_skip:
                name = _pygame_key_to_name(event)
                _pressed_keys[event.key] = name
                _keys_pressed_this_frame.append(name)
        if event.type == pygame.KEYUP:  # pylint: disable=no-member
            if not (event.key in _keys_to_skip) and event.key in _pressed_keys:
                _keys_released_this_frame.append(_pressed_keys[event.key])
                del _pressed_keys[event.key]

    ############################################################
    # @when_any_key_pressed and @when_key_pressed callbacks
    ############################################################
    for key in _keys_pressed_this_frame:
        for callback in _keypress_callbacks:
            if not callback.is_running and (
                    callback.keys is None or key in callback.keys
            ):
                _loop.create_task(callback(key))

    ############################################################
    # @when_any_key_released and @when_key_released callbacks
    ############################################################
    for key in _keys_released_this_frame:
        for callback in _keyrelease_callbacks:
            if not callback.is_running and (
                    callback.keys is None or key in callback.keys
            ):
                _loop.create_task(callback(key))

    ####################################
    # @mouse.when_clicked callbacks
    ####################################
    if click_happened_this_frame and mouse._when_clicked_callbacks:
        for callback in mouse._when_clicked_callbacks:
            _loop.create_task(callback())

    ########################################
    # @mouse.when_click_released callbacks
    ########################################
    if click_release_happened_this_frame and mouse._when_click_released_callbacks:
        for callback in mouse._when_click_released_callbacks:
            _loop.create_task(callback())

    #############################
    # @repeat_forever callbacks
    #############################
    for callback in _repeat_forever_callbacks:
        if not callback.is_running:
            _loop.create_task(callback())

    #############################
    # physics simulation
    #############################
    _loop.call_soon(simulate_physics)

    # 1.  get pygame events
    #       - set mouse position, clicked, keys pressed, keys released
    # 2.  run when_program_starts callbacks
    # 3.  run physics simulation
    # 4.  compute new pygame_surfaces (scale, rotate)
    # 5.  run repeat_forever callbacks
    # 6.  run mouse/click callbacks (make sure more than one isn't running at a time)
    # 7.  run keyboard callbacks (make sure more than one isn't running at a time)
    # 8.  run when_touched callbacks
    # 9.  render background
    # 10. render sprites (with correct z-order)
    # 11. call event loop again

    PYGAME_DISPLAY.fill(_color_name_to_rgb(backdrop))

    # BACKGROUND COLOR
    # note: cannot use screen.fill((1, 1, 1)) because pygame's screen
    #       does not support fill() on OpenGL surfaces
    # gl.glClearColor(_background_color[0], _background_color[1], _background_color[2], 1)
    # gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    for sprite in all_sprites:

        sprite._is_clicked = False

        if sprite.is_hidden:
            continue

        ######################################################
        # update sprites with results of physics simulation
        ######################################################
        if sprite.physics and sprite.physics.can_move:

            body = sprite.physics._pymunk_body
            angle = _math.degrees(body.angle)
            if isinstance(sprite, Line):
                sprite._x = body.position.x - (sprite.length / 2) * _math.cos(angle)
                sprite._y = body.position.y - (sprite.length / 2) * _math.sin(angle)
                sprite._x1 = body.position.x + (sprite.length / 2) * _math.cos(angle)
                sprite._y1 = body.position.y + (sprite.length / 2) * _math.sin(angle)
                # sprite._length, sprite._angle = sprite._calc_length_angle()
            else:
                if (
                        str(body.position.x) != "nan"
                ):  # this condition can happen when changing sprite.physics.can_move
                    sprite._x = body.position.x
                if str(body.position.y) != "nan":
                    sprite._y = body.position.y

            sprite.angle = (
                angle  # needs to be .angle, not ._angle so surface gets recalculated
            )
            sprite.physics._x_speed, sprite.physics._y_speed = body.velocity

        #################################
        # @sprite.when_clicked events
        #################################
        if mouse.is_clicked and not isinstance(sprite, Line):
            if point_touching_sprite(mouse, sprite) and click_happened_this_frame:
                # only run sprite clicks on the frame the mouse was clicked
                sprite._is_clicked = True
                for callback in sprite._when_clicked_callbacks:
                    if not callback.is_running:
                        _loop.create_task(callback())

        # do sprite image transforms (re-rendering images/fonts, scaling, rotating, etc)

        # we put it in the event loop instead of just recomputing immediately because if we do it
        # synchronously then the data and rendered image may get out of sync
        if sprite._should_recompute_primary_surface:
            # recomputing primary surface also recomputes secondary surface
            _loop.call_soon(sprite._compute_primary_surface)
        elif sprite._should_recompute_secondary_surface:
            _loop.call_soon(sprite._compute_secondary_surface)

        if isinstance(sprite, Line):
            # @hack: Line-drawing code should probably be in the line._compute_primary_surface function
            # but the coordinates work different for lines than other sprites.

            # x = screen.width/2 + sprite.x
            # y = screen.height/2 - sprite.y - sprite.thickness
            # _pygame_display.blit(sprite._secondary_pygame_surface, (x,y) )

            x = screen.width / 2 + sprite.x  # pylint: disable=invalid-name
            y = screen.height / 2 - sprite.y  # pylint: disable=invalid-name
            x_1 = screen.width / 2 + sprite.x1
            y_1 = screen.height / 2 - sprite.y1
            if sprite.thickness == 1:
                pygame.draw.aaline(
                    PYGAME_DISPLAY,
                    _color_name_to_rgb(sprite.color),
                    (x, y),
                    (x_1, y_1),
                    True,
                )
            else:
                pygame.draw.line(
                    PYGAME_DISPLAY,
                    _color_name_to_rgb(sprite.color),
                    (x, y),
                    (x_1, y_1),
                    sprite.thickness,
                )
        else:

            PYGAME_DISPLAY.blit(
                sprite._secondary_pygame_surface,
                (sprite._pygame_x(), sprite._pygame_y()),
            )

    pygame.display.flip()
    _loop.call_soon(_game_loop)
    return True


# @decorator
def when_program_starts(func):
    """
    Call code right when the program starts.

    Used like this:

    @play.when_program_starts
    def do():
        print('the program just started!')
    :param func: The function to call when the program starts.
    :return: The decorator function.
    """
    async_callback = _make_async(func)

    async def wrapper(*args, **kwargs):
        return await async_callback(*args, **kwargs)

    _when_program_starts_callbacks.append(wrapper)
    return func


def repeat(number_of_times):
    """
    Repeat a set of commands a certain number of times.

    Equivalent to `range(1, number_of_times+1)`.

    Used like this:

    @play.repeat_forever
    async def do():
        for count in play.repeat(10):
            print(count)
    :param number_of_times: The number of times to repeat the commands.
    :return: A range object that can be iterated over.
    """
    return range(1, number_of_times + 1)


def start_program():
    """
    Calling this function starts your program running.

    play.start_program() should almost certainly go at the very end of your program.
    """
    for func in _when_program_starts_callbacks:
        _loop.create_task(func())

    _loop.call_soon(_game_loop)
    try:
        _loop.run_forever()
    finally:
        _logging.getLogger("asyncio").setLevel(_logging.CRITICAL)
        pygame.quit()  # pylint: disable=no-member


_repeat_forever_callbacks = []


# @decorator
def repeat_forever(func):
    """
    Calls the given function repeatedly in the game loop.

    Example:

        text = play.new_text(words='hi there!', x=0, y=0, font='Arial.ttf', font_size=20, color='black')

        @play.repeat_forever
        async def do():
            text.turn(degrees=15)
    :param func: The function to call repeatedly.
    :return: The decorator function.
    """
    async_callback = _make_async(func)

    async def repeat_wrapper():
        repeat_wrapper.is_running = True
        await async_callback()
        repeat_wrapper.is_running = False

    repeat_wrapper.is_running = False
    _repeat_forever_callbacks.append(repeat_wrapper)
    return func


# @decorator
def when_sprite_clicked(*sprites):
    """A decorator that runs a function when a sprite is clicked.
    :param sprites: The sprites to run the function on.
    :return: The function to run.
    """

    def wrapper(func):
        for sprite in sprites:
            sprite.when_clicked(func, call_with_sprite=True)
        return func

    return wrapper


# @decorator
def when_any_key_pressed(func):
    if not callable(func):
        raise Oops(
            """@play.when_any_key_pressed doesn't use a list of keys. Try just this instead:

@play.when_any_key_pressed
async def do(key):
    print("This key was pressed!", key)
"""
        )
    async_callback = _make_async(func)

    async def wrapper(*args, **kwargs):
        wrapper.is_running = True
        await async_callback(*args, **kwargs)
        wrapper.is_running = False

    wrapper.keys = None
    wrapper.is_running = False
    _keypress_callbacks.append(wrapper)
    return wrapper


# @decorator
def when_key_pressed(*keys):
    def decorator(func):
        async_callback = _make_async(func)

        async def wrapper(*args, **kwargs):
            wrapper.is_running = True
            await async_callback(*args, **kwargs)
            wrapper.is_running = False

        wrapper.keys = keys
        wrapper.is_running = False
        _keypress_callbacks.append(wrapper)
        return wrapper

    return decorator


# @decorator
def when_any_key_released(func):
    if not callable(func):
        raise Oops(
            """@play.when_any_key_released doesn't use a list of keys. Try just this instead:

@play.when_any_key_released
async def do(key):
    print("This key was released!", key)
"""
        )
    async_callback = _make_async(func)

    async def wrapper(*args, **kwargs):
        wrapper.is_running = True
        await async_callback(*args, **kwargs)
        wrapper.is_running = False

    wrapper.keys = None
    wrapper.is_running = False
    _keyrelease_callbacks.append(wrapper)
    return wrapper


# @decorator
def when_key_released(*keys):
    def decorator(func):
        async_callback = _make_async(func)

        async def wrapper(*args, **kwargs):
            wrapper.is_running = True
            await async_callback(*args, **kwargs)
            wrapper.is_running = False

        wrapper.keys = keys
        wrapper.is_running = False
        _keyrelease_callbacks.append(wrapper)
        return wrapper

    return decorator
