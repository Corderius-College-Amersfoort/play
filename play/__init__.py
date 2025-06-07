"""The library to make pygame easier to use."""

import warnings
from .api import *
from .io.controllers import controllers
from .io.mouse import mouse

warnings.filterwarnings("ignore", category=UserWarning, module=r"cffi\.cparser")
