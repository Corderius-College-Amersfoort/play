"""Global variables for the game"""

import pygame


class Globals:  # pylint: disable=too-few-public-methods
    all_sprites = []
    sprites_group = pygame.sprite.Group()

    walls = []

    backdrop_type = "color"  # color or image
    backdrop = (255, 255, 255)

    FRAME_RATE = 60
    WIDTH = 800
    HEIGHT = 600

    gravity = None
    num_sim_steps = 10

    display = None  # This will be set in the screen module
    controllers = []

globals_list = Globals()
