"""Core game loop and event handling functions."""

import pygame  # pylint: disable=import-error

from .game_loop_wrapper import listen_to_failure
from .mouse_loop import _handle_mouse_loop, mouse_state
from .sprites_loop import _update_sprites
from ..callback import callback_manager, CallbackType
from ..callback.callback_helpers import run_callback
from ..globals import backdrop, FRAME_RATE, _walls
from ..io import screen, PYGAME_DISPLAY, convert_pos
from ..io.keypress import (
    key_num_to_name as _pygame_key_to_name,
    _keys_released_this_frame,
    _keys_to_skip,
    _pressed_keys,
)  # don't pollute user-facing namespace with library internals
from ..io.mouse import mouse
from .physics_loop import simulate_physics
from ..utils import color_name_to_rgb as _color_name_to_rgb
from ..loop import loop as _loop
from .controller_loop import (
    controller_axis_moved,
    controller_button_pressed,
    controller_button_released,
    _handle_controller,
    _handle_controller_events,
)

_clock = pygame.time.Clock()


def _handle_pygame_events():
    """Handle pygame events in the game loop."""
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
            mouse_state.click_happened_this_frame = True
            mouse._is_clicked = True
        if event.type == pygame.MOUSEBUTTONUP:  # pylint: disable=no-member
            mouse_state.click_release_happened_this_frame = True
            mouse._is_clicked = False
        if event.type == pygame.MOUSEMOTION:  # pylint: disable=no-member
            mouse.x, mouse.y = (event.pos[0] - screen.width / 2.0), (
                screen.height / 2.0 - event.pos[1]
            )
        _handle_controller_events(event)
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
    if (
        _pressed_keys
        and callback_manager.get_callbacks(CallbackType.PRESSED_KEYS) is not None
    ):
        press_subscription = callback_manager.get_callbacks(CallbackType.PRESSED_KEYS)
        for key in _pressed_keys:
            if key in callback_manager.get_callbacks(CallbackType.PRESSED_KEYS):
                for callback in press_subscription[key]:
                    if not callback.is_running:
                        run_callback(
                            callback,
                            ["key"],
                            [],
                            key,
                        )
            if "any" in press_subscription:
                for callback in press_subscription["any"]:
                    if not callback.is_running:
                        run_callback(
                            callback,
                            ["key"],
                            [],
                            key,
                        )
        keys_hash = hash(frozenset(_pressed_keys))
        if keys_hash in press_subscription:
            for callback in press_subscription[keys_hash]:
                if not callback.is_running:
                    run_callback(
                        callback,
                        ["key"],
                        [],
                        _pressed_keys,
                    )

    ############################################################
    # @when_any_key_released and @when_key_released callbacks
    ############################################################
    if _keys_released_this_frame and callback_manager.get_callbacks(
        CallbackType.RELEASED_KEYS
    ):
        release_subscriptions = callback_manager.get_callbacks(
            CallbackType.RELEASED_KEYS
        )
        for key in _keys_released_this_frame:
            if key in release_subscriptions:
                for callback in release_subscriptions[key]:
                    if not callback.is_running:
                        run_callback(
                            callback,
                            ["key"],
                            [],
                            key,
                        )
            if "any" in release_subscriptions:
                for callback in release_subscriptions["any"]:
                    if not callback.is_running:
                        run_callback(
                            callback,
                            ["key"],
                            [],
                            key,
                        )


# pylint: disable=too-many-branches, too-many-statements
@listen_to_failure()
def game_loop():
    """The main game loop."""
    _keys_released_this_frame.clear()
    mouse_state.click_happened_this_frame = False
    mouse_state.click_release_happened_this_frame = False

    _clock.tick(FRAME_RATE)

    if not _handle_pygame_events():
        return False

    _handle_keyboard()

    if (
        mouse_state.click_happened_this_frame
        or mouse_state.click_release_happened_this_frame
    ):
        _handle_mouse_loop()

    _handle_controller()

    #############################
    # @repeat_forever callbacks
    #############################
    if callback_manager.get_callbacks(CallbackType.REPEAT_FOREVER) is not None:
        for callback in callback_manager.get_callbacks(CallbackType.REPEAT_FOREVER):
            if not callback.is_running:
                run_callback(
                    callback,
                    [],
                    [],
                )

    #############################
    # physics simulation
    #############################
    _loop.call_soon(simulate_physics)

    PYGAME_DISPLAY.fill(_color_name_to_rgb(backdrop))

    _update_sprites()

    _loop.call_soon(game_loop)
    for wall in _walls:
        actual_rect = [*convert_pos(*wall.a), *convert_pos(*wall.b)]

        actual_rect = pygame.Rect(
            min(actual_rect[0], actual_rect[2]) - 2,
            min(actual_rect[1], actual_rect[3]) - 2,
            abs(actual_rect[0] - actual_rect[2]) + 6,
            abs(actual_rect[1] - actual_rect[3]) + 6,
        )
        pygame.draw.rect(PYGAME_DISPLAY, (0, 0, 0), actual_rect, 2)
    pygame.display.flip()
    return True
