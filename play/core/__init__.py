"""Core game loop and event handling functions."""

import math as _math

import pygame  # pylint: disable=import-error

from ..globals import backdrop, FRAME_RATE, sprites_group
from ..io import screen, PYGAME_DISPLAY
from ..io.keypress import (
    key_num_to_name as _pygame_key_to_name,
    _keys_released_this_frame,
    _keys_to_skip,
    _pressed_keys,
    _pressed_keys_subscriptions,
    _release_keys_subscriptions,
)  # don't pollute user-facing namespace with library internals
from ..io.mouse import mouse
from ..objects.line import Line
from ..objects.sprite import point_touching_sprite
from ..physics import simulate_physics
from ..utils import color_name_to_rgb as _color_name_to_rgb
from ..loop import loop as _loop

_repeat_forever_callbacks = []
_when_program_starts_callbacks = []
_clock = pygame.time.Clock()

click_happened_this_frame = False  # pylint: disable=invalid-name
click_release_happened_this_frame = False  # pylint: disable=invalid-name


def _handle_pygame_events():
    """Handle pygame events in the game loop."""
    global click_happened_this_frame
    global click_release_happened_this_frame

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
                if name not in _pressed_keys:
                    _pressed_keys.append(name)
        if event.type == pygame.KEYUP:  # pylint: disable=no-member
            name = _pygame_key_to_name(event)
            if not (event.key in _keys_to_skip) and name in _pressed_keys:
                _keys_released_this_frame.append(name)
                _pressed_keys.remove(name)
    return True


# pylint: disable=too-many-branches
def _handle_keyboard():
    """Handle keyboard events in the game loop."""
    ############################################################
    # @when_any_key_pressed and @when_key_pressed callbacks
    ############################################################
    if _pressed_keys:
        for key in _pressed_keys:
            if key in _pressed_keys_subscriptions:
                for callback in _pressed_keys_subscriptions[key]:
                    if not callback.is_running:
                        _loop.create_task(callback(key))
            if "any" in _pressed_keys_subscriptions:
                for callback in _pressed_keys_subscriptions["any"]:
                    if not callback.is_running:
                        _loop.create_task(callback(key))
        keys_hash = hash(frozenset(_pressed_keys))
        if keys_hash in _pressed_keys_subscriptions:
            for callback in _pressed_keys_subscriptions[keys_hash]:
                if not callback.is_running:
                    _loop.create_task(callback(_pressed_keys))

    ############################################################
    # @when_any_key_released and @when_key_released callbacks
    ############################################################
    for key in _keys_released_this_frame:
        if key in _release_keys_subscriptions:
            for callback in _release_keys_subscriptions[key]:
                if not callback.is_running:
                    _loop.create_task(callback(key))
        if "any" in _release_keys_subscriptions:
            for callback in _release_keys_subscriptions["any"]:
                if not callback.is_running:
                    _loop.create_task(callback(key))


def _handle_mouse_loop():
    """Handle mouse events in the game loop."""
    ####################################
    # @mouse.when_clicked callbacks
    ####################################
    if mouse._when_clicked_callbacks:
        for callback in mouse._when_clicked_callbacks:
            _loop.create_task(callback())

    ########################################
    # @mouse.when_click_released callbacks
    ########################################
    if mouse._when_click_released_callbacks:
        for callback in mouse._when_click_released_callbacks:
            _loop.create_task(callback())


def _update_sprites():
    for sprite in sprites_group.sprites():
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
        if mouse.is_clicked:

            if (
                point_touching_sprite((mouse.x, mouse.y), sprite)
                and click_happened_this_frame
            ):
                # only run sprite clicks on the frame the mouse was clicked
                sprite._is_clicked = True
                for callback in sprite._when_clicked_callbacks:
                    if not callback.is_running:
                        _loop.create_task(callback())

        #################################
        # @sprite.when_touching events
        #################################
        if sprite._active_callbacks:
            for cb in sprite._active_callbacks:
                _loop.create_task(cb())

    sprites_group.update()
    sprites_group.draw(PYGAME_DISPLAY)


# pylint: disable=too-many-branches, too-many-statements
def game_loop():
    """The main game loop."""
    _keys_released_this_frame.clear()
    global click_happened_this_frame, click_release_happened_this_frame
    click_happened_this_frame = False
    click_release_happened_this_frame = False

    _clock.tick(FRAME_RATE)

    if not _handle_pygame_events():
        return False

    _handle_keyboard()

    if click_happened_this_frame or click_release_happened_this_frame:
        _handle_mouse_loop()

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

    PYGAME_DISPLAY.fill(_color_name_to_rgb(backdrop))

    _update_sprites()

    pygame.display.flip()
    _loop.call_soon(game_loop)
    return True
