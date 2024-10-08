"""This module is used to create a global event loop for the application."""

import asyncio as _asyncio

_loop = _asyncio.get_event_loop()
_loop.set_debug(False)
