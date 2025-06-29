"""This module contains the function that simulates the physics of the game"""

from .sprites_loop import update_sprites
from ..globals import globals_list
from ..physics import physics_space


async def simulate_physics():
    """
    Simulate the physics of the game
    """
    # more steps means more accurate simulation but more processing time
    for _ in range(globals_list.num_sim_steps):
        physics_space.step(1 / (globals_list.FRAME_RATE * globals_list.num_sim_steps))
        if not _ == globals_list.num_sim_steps - 1:
            await update_sprites(False)
