"""
Logger configuration module.
Sets up a logger to be used across the project for consistent logging.
"""

import logging
import sys


def setup_logger(name: str, level: int = logging.DEBUG, stream: bool = True) -> logging.Logger:
    """
    Sets up a logger with the given name and configuration options.

    Args:
        name (str): Name of the logger, usually the module's __name__.
        level (int): Logging level for the logger. Default is logging.DEBUG.
        stream (bool): If True, adds a StreamHandler to output logs to stdout. Default is True.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a handler for outputting logs
    handler: logging.Handler
    if stream:
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.FileHandler("app.log")  # Example for file logging

    handler.setLevel(level)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger
