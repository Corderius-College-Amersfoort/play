"""
Logging module for the play package.
"""

import logging


class LogFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + _format + reset,
        logging.INFO: grey + _format + reset,
        logging.WARNING: yellow + _format + reset,
        logging.ERROR: red + _format + reset,
        logging.CRITICAL: bold_red + _format + reset,
    }

    def format(self, record):
        """
        Format the log record.
        :param record: The log record to format.
        :return: The formatted log record.
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


play_logger = logging.getLogger("play")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(LogFormatter())
play_logger.addHandler(ch)
play_logger.setLevel(logging.DEBUG)
