"""The library to make pygame easier to use."""

import warnings
import pygame


from .api import *
from .io.controllers import controllers
from .io.mouse import mouse

pygame.init()
warnings.filterwarnings("ignore", category=UserWarning, module=r"cffi\.cparser")
