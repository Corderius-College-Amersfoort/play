"""The library to make pygame easier to use."""

import warnings
from .api import *

warnings.filterwarnings("ignore", category=UserWarning, module=r"cffi\.cparser")
