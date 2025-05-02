import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str = "TrackLogger", log_dir: str = ".") -> logging.Logger:
    """
    Sets up a logger with both activity and error file handlers.
    Args:
        name: Name of the logger.
        log_dir: Directory where log files will be stored.
    Returns:
        Configured logger.
    """
    logger = logging.getLogger(name)

    if logger.handlers:  # Prevent adding duplicate handlers
        return logger

    logger.setLevel(logging.INFO)

    os.makedirs(log_dir, exist_ok=True)

    # Activity logger
    activity_handler = RotatingFileHandler(
        os.path.join(log_dir, "activity.log"),
        maxBytes=1_000_000,
        backupCount=5
    )
    activity_handler.setLevel(logging.INFO)
    activity_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Error logger
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, "errors.log"),
        maxBytes=1_000_000,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Console logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger.addHandler(activity_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    return logger
