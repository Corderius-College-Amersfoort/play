"""The library to make pygame easier to use."""

import warnings
from .api import *
from .io.screen import screen

warnings.filterwarnings("ignore", category=UserWarning, module=r"cffi\.cparser")
