"""
This module contains the API for the game.
"""

from .generators import (
    new_text,
    new_box,
    new_circle,
    new_line,
    new_image,
    new_sound,
    new_database,
)
from .events import (
    when_program_starts,
    repeat_forever,
    when_sprite_clicked,
    when_any_key_pressed,
    when_key_pressed,
    when_any_key_released,
    when_key_released,
    when_mouse_clicked,
    when_click_released,
)
from .utils import (
    start_program,
    stop_program,
    animate,
    set_backdrop,
    set_backdrop_image,
    timer,
    key_is_pressed,
    set_physics_simulation_steps,
)
from .random import random_number, random_color, random_position
