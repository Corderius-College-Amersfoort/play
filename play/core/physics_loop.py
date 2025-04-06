"""This module contains the function that simulates the physics of the game"""

from ..globals import globals_list
from ..physics import physics_space


def simulate_physics() -> None:
    """
    Simulate the physics of the game
    """
    physics_space.step(1 / globals_list.FRAME_RATE)
