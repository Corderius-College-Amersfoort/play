"""This module contains the function that simulates the physics of the game"""

from .sprites_loop import _update_sprites
from ..globals import globals_list
from ..physics import physics_space, _NUM_SIMULATION_STEPS


async def simulate_physics():
    """
    Simulate the physics of the game
    """
    # more steps means more accurate simulation, but more processing time
    for _ in range(_NUM_SIMULATION_STEPS):
        physics_space.step(1 / (globals_list.FRAME_RATE * _NUM_SIMULATION_STEPS))
        if not _ == _NUM_SIMULATION_STEPS - 1:
            await _update_sprites(False)
