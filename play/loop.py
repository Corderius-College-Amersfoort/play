"""This module is used to create a global event loop for the application."""

import asyncio as _asyncio

loop = _asyncio.get_event_loop()
loop.set_debug(False)
